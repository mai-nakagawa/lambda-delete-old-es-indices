import os
import boto3
from datetime import datetime, timedelta
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import logging
import curator

logger = logging.getLogger('curator')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

service = 'es'
credentials = boto3.Session().get_credentials()

def lambda_handler(event, context):

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        os.environ['region'],
        service,
        session_token=credentials.token
    )
    es = Elasticsearch(
        hosts = [{'host': os.environ['host'], 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection,
        timeout = 120
    )

    # retention_daysより古いindexを削除する
    try:
        index_list = curator.IndexList(es)
        index_list.filter_by_regex(kind='prefix', value=os.environ['index_prefix'])
        index_list.filter_by_age(
            source = 'name',
            direction = 'older',
            timestring = os.environ['date_string'],
            unit = 'days',
            unit_count = int(os.environ['retention_days']) + 1
        )
        curator.DeleteIndices(index_list, master_timeout=180).do_action()
    except curator.exceptions.NoIndices as e:
        logging.info("No indices to delete")
    except curator.exceptions.FailedExecution as e:
        logging.error("Failed to delete indices", exc_info=True)

# For test
if __name__ == '__main__':
    os.environ['host'] = '' # For example, search-my-domain.region.es.amazonaws.com
    os.environ['region'] = '' # For example, us-west-1
    os.environ['index_prefix'] = ''
    os.environ['date_string'] = '' # For example, %Y-%m-%d
    os.environ['retention_days'] = '' # For example, 30
    lambda_handler({}, None)
