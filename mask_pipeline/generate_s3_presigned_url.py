#Reference https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
import sys
import boto3
from botocore.exceptions import ClientError
from masks_aws_credentials import *

def create_presigned_url(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        raise ValueError(e)
        return None

    # The response contains the presigned URL
    return response


if __name__ == '__main__':

    bucket_name = sys.argv[1]
    object_name = sys.argv[2]

    print('Running generate_s3_presigned_url.py with following parameters')
    print(f'bucket_name: {bucket_name}')
    print(f'object_name: {object_name}')

    print(create_presigned_url(bucket_name, object_name))
