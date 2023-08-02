import json
from typing import Dict

import boto3


def get_secret(secret_category: str, secret_name: str) -> str | None:
    # Create a Secrets Manager client
    secrets_client = boto3.client("secretsmanager", region_name="ap-northeast-1")

    # Retrieve the secret value
    response = secrets_client.get_secret_value(SecretId=secret_category)
    secrets: Dict = json.loads(response["SecretString"])
    token: str = secrets[secret_name]
    if token == "":
        return None
    return token
