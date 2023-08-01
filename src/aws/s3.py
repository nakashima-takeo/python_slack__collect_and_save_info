from datetime import datetime

import boto3


class S3:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def write_txt(self, bucket_name: str, file_title: str, file_contents: str) -> None:
        key = "file_title_" + datetime.now().strftime("%Y-%m-%d-%H") + ".txt"
        obj = self.s3.Object(bucket_name, key)
        obj.put(Body=file_contents)
        return
