from datetime import datetime

import boto3


class S3:
    """
    AWS S3を操作するクラス
    """

    def __init__(self):
        self.__s3 = boto3.resource("s3")
        self.__s3_client = boto3.client("s3")

    def write_txt(self, bucket_name: str, file_title_head: str, file_contents: str) -> str:
        """
        テキストファイルをS3に書き込む

        Parameters
        ----------
        bucket_name : str
          保存先バケット名
        file_title_head : str
          保存する時のファイル名
        file_contents : str
          テキストファイルの中身

        Returns
        -------
        str
          書き込んだファイルの公開URL
        """
        key = f"{file_title_head}_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
        obj = self.__s3.Object(bucket_name, key)
        obj.put(Body=file_contents)
        public_url = self.__get_public_url(bucket_name, key)
        return public_url

    def __get_public_url(self, bucket, target_object_path) -> str:
        """
        プライベートメソッド
        S3オブジェクトの公開URLを取得する

        Parameters
        ----------
        bucket : str
          オブジェクトがあるバケットの名前
        target_object_path : str
          オブジェクトのパス

        Returns
        -------
        str
          オブジェクトの公開URL
        """
        bucket_location = self.__s3_client.get_bucket_location(Bucket=bucket)
        return "https://{0}.s3.{1}.amazonaws.com/{2}".format(bucket, bucket_location["LocationConstraint"], target_object_path)
