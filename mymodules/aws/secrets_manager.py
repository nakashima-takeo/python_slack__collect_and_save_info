import json
from typing import Dict

import boto3


class SecretsManager:
    """
    AWS Secrets Managerを操作するクラス
    """

    def __init__(self, region_name: str = "ap-northeast-1"):
        # Secrets Managerクライアントを作成する
        self.__secrets_client = boto3.client("secretsmanager", region_name=region_name)

    def get_secret(self, secret_category: str, secret_name: str) -> str | None:
        """
        シークレットの値を取得します。

        Parameters
        ----------
        secret_category : str
          取得するシークレットのカテゴリ。
        secret_name : str
          取得するシークレットの名前。

        Returns
        -------
        str or None
          シークレットの値。シークレットが見つからない場合や空の値の場合はNoneを返します。

        """
        # シークレットの値を取得する
        response = self.__secrets_client.get_secret_value(SecretId=secret_category)
        secrets: Dict = json.loads(response["SecretString"])
        token: str = secrets[secret_name]
        if token == "":
            return None
        return token
