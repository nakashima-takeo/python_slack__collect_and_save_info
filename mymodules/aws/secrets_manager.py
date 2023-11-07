import json
from typing import Dict

import boto3


class SecretsManager:
    def __init__(self):
        # Create a Secrets Manager client
        self.secrets_client = boto3.client("secretsmanager", region_name="ap-northeast-1")

    def get_secret(self, secret_category: str, secret_name: str) -> str | None:
        # Retrieve the secret value
        response = self.secrets_client.get_secret_value(SecretId=secret_category)
        secrets: Dict = json.loads(response["SecretString"])
        token: str = secrets[secret_name]
        if token == "":
            return None
        return token
