import boto3
import botocore
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--web-instance-name",
    type=str,
    help="Value of 'Name' tag of the web tier instance to be terminated",
)
parser.add_argument(
    "--in-bucket-name",
    type=str,
    help="Value of 'Name' tag of the S3 input bucket to be terminated",
)
parser.add_argument(
    "--out-bucket-name",
    type=str,
    help="Value of 'Name' tag of the S3 output bucket to be terminated",
)
parser.add_argument(
    "--in-queue-name",
    type=str,
    help="Value of 'Name' tag of the SQS request queue to be terminated",
)
parser.add_argument(
    "--out-queue-name",
    type=str,
    help="Value of 'Name' tag of the SQS response queue to be terminated",
)
args = vars(parser.parse_args())


def noneparser(obj, key):
    return str(obj[key]) if obj.get(key) else None


target_web_instance_name = noneparser(args, "web_instance_name")
target_in_bucket_name = noneparser(args, "in_bucket_name")
target_out_bucket_name = noneparser(args, "out_bucket_name")
target_in_queue_name = noneparser(args, "in_queue_name")
target_out_queue_name = noneparser(args, "out_queue_name")

print(
    target_web_instance_name,
    target_in_bucket_name,
    target_out_bucket_name,
    target_in_queue_name,
    target_out_queue_name,
)

# creds from ~/.aws/credentials
session = boto3.Session(profile_name="dev")

region1 = "us-east-1"
dev_ec2_client = session.client("ec2", region_name=region1)
dev_s3_client = session.client("s3", region_name=region1)


def get_instance_id_by_name_tag(name):
    all_instances = dev_ec2_client.describe_instances()
    for reservation in all_instances["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name" and tag["Value"] == name:
                    return instance["InstanceId"]
    return -1

# web tier
if target_web_instance_name is not None:
    target_inst_id = get_instance_id_by_name_tag(target_web_instance_name)
    if target_inst_id == -1:
        print("Instance does not exist")
    else:
        print("Found web-instance ID: ", target_inst_id)
        response = dev_ec2_client.terminate_instances(InstanceIds=[target_inst_id])
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("Terminated instance successfully")

# buckets
if target_in_bucket_name is not None:
    try:
        response = dev_s3_client.delete_bucket(Bucket=target_in_bucket_name)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            print("Deleted input bucket successfully")
    except dev_s3_client.exceptions.NoSuchBucket as e:
        print("Input bucket does not exist")
if target_out_bucket_name is not None:
    try:
        response = dev_s3_client.delete_bucket(Bucket=target_out_bucket_name)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            print("Deleted output bucket successfully")
    except dev_s3_client.exceptions.NoSuchBucket as e:
        print("Output bucket does not exist")