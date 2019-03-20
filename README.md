# lambda-delete-old-es-indices

This is a lambda function of AWS Lambda. It deletes indices of Elasticsearch making use of elasticsearch-curator Python API.

# How to run on AWS Lambda
1. `pip install requests_aws4auth -t .`
1. `pip install elasticsearch-curator -t .`
1. `zip -r lambda-delete-old-es-indices.zip .`
1. Create a lambda function with the zip file
1. Set the following environmental variables:
  - host (e.g. search-my-domain.region.es.amazonaws.com)
  - region (e.g. ap-northeast-1)
  - index_prefix
  - date_string (e.g. %Y-%m-%d)
  - retention_days (e.g. 30)

# How to test locally
1. Configure those environmental variable in the main function of `lambda_function.py`
1. Execute `PYTHONPATH=. python lambda_function.py`
