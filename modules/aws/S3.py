from datetime import datetime

import boto3


class S3:
    def __init__(self):
        self.s3 = boto3.resource("s3")
        self.s3_client = boto3.client("s3")

    def write_txt(self, bucket_name: str, file_title_head: str, file_contents: str) -> str:
        key = f"{file_title_head}_" + datetime.now().strftime("%Y-%m-%d-%H") + ".txt"
        obj = self.s3.Object(bucket_name, key)
        obj.put(Body=file_contents)
        public_url = self.__get_public_url(bucket_name, key)
        return public_url

    def __get_public_url(self, bucket, target_object_path) -> str:
        bucket_location = self.s3_client.get_bucket_location(Bucket=bucket)
        return "https://{0}.s3.{1}.amazonaws.com/{2}".format(bucket, bucket_location["LocationConstraint"], target_object_path)
