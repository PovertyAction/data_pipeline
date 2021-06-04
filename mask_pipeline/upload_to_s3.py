# import logging
import boto3
from botocore.exceptions import ClientError
from masks_aws_credentials import *
import sys
import os

def upload_file(file_name, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    # Upload the file

    s3_client = boto3.client('s3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
        )

    try:
        response = s3_client.upload_file(file_name, bucket, os.path.basename(file_name))
    except ClientError as e:
        raise ValueError(e)
    return True


if __name__ == '__main__':


    file_to_upload = sys.argv[1]
    bucket = sys.argv[2]

    upload_file(file_to_upload, bucket)
