import json
from typing import Dict

import boto3


class ParameterStore:
    """
    AWS Systems Managerのパラメータストアを操作するクラス

    Parameters
    ----------
    region_name : str, optional
      AWSリージョン名, by default "ap-southeast-2"
    """

    def __init__(self, region_name: str = "ap-southeast-2"):
        """
        Parameters
        ----------
        region_name : str, optional
          AWSリージョン名, by default "ap-southeast-2"
        """
        # Systems Managerクライアントを作成する
        self.__ssm = boto3.client("ssm", region_name=region_name)

    def get_parameter(self, parameter_name: str) -> Dict:
        """
        指定されたパラメータ名のパラメータを取得する

        Parameters
        ----------
        parameter_name : str
          パラメータ名

        Returns
        -------
        Dict
          パラメータの辞書オブジェクト
        """
        return json.loads(self.__ssm.get_parameter(Name=parameter_name, WithDecryption=True)["Parameter"][0]["Value"])
