import json
import boto3

def get_secret(secret_name):
    # Create a Secrets Manager client
    secrets_client = boto3.client('secretsmanager', region_name='ap-northeast-1')

    # Retrieve the secret value
    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret = json.load(response['SecretString'])
    return secret
