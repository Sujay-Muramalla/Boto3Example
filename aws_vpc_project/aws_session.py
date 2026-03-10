import boto3
from config import AWS_REGION


def get_ec2_resource():
    return boto3.resource("ec2", region_name=AWS_REGION)