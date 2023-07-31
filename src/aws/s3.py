import boto3


class S3:
    def __init__(self):
        self.s3 = boto3.client("s3")
