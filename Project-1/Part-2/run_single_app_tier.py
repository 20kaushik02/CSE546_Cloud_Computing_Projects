import boto3
from pathlib import Path


# creds from ~/.aws/credentials
session = boto3.Session(profile_name="dev")
dev_ec2_client = session.client("ec2", region_name="us-east-1")

# Ubuntu Server 22.04 LTS, 8GB SSD on EBS, 64-bit (x86) 1vCPU
# pip installed, torch installed, model loaded
app_tier_ami_id = "ami-05afaa0d246abf7cf"
reservation = dev_ec2_client.run_instances(
    ImageId=app_tier_ami_id,
    InstanceType="t2.micro",
	KeyName='cse546-dev',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": "app-tier-instance"}]}
    ],
	# UserData=user_data
)

print("Instances allocated successfully:", "Yes" if reservation else "No")
