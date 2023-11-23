import boto3


class ParameterStore:
    """
    AWS Systems Managerのパラメータストアを操作するクラス

    Parameters
    ----------
    region_name : str
      AWSリージョン名
    """

    def __init__(self, region_name: str):
        # Systems Managerクライアントを作成する
        self.__ssm = boto3.client("ssm", region_name=region_name)

    def get_parameter(self, parameter_name: str) -> str:
        """
        指定されたパラメータ名のパラメータを取得する

        Parameters
        ----------
        parameter_name : str
          パラメータ名

        Returns
        -------
        str
          パラメータの値
        """
        return self.__ssm.get_parameter(Name=parameter_name, WithDecryption=True)["Parameter"]["Value"]
