import boto3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--eip-id", type=str,help="Allocation ID of elastic IP address")
args = vars(parser.parse_args())
eip_id = str(args["eip-id"]) if args.get("eip-id") else None

# creds from ~/.aws/credentials
session = boto3.Session(profile_name="dev")
dev_ec2_client = session.client("ec2", region_name="us-east-1")

with open(Path(__file__) / ".." / "web_tier_instance_run", "r") as setup_f:
	user_data = setup_f.read()
	
# Create capacity reservation of instances
ami_id = "ami-0c7217cdde317cfec" # Ubuntu Server 22.04 LTS, 8GB SSD on EBS, 64-bit (x86) 1vCPU
reservation = dev_ec2_client.run_instances(
    ImageId=ami_id,
    InstanceType="t2.micro",
	KeyName='cse546-dev',
    MinCount=1,  # if available instances are less than min_count, abort with no allocation
    MaxCount=1,  # try to allocate max_count instances. we only need one for now
    TagSpecifications=[
        {"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": "web-instance"}]}
    ],
	# UserData=user_data
)

print("Instances allocated successfully:", "Yes" if reservation else "No")
new_inst_id = ''

# Allocate EIP on successful instance launch
if reservation and eip_id is not None:
	print("Waiting for instance to start running...")
	waiter = dev_ec2_client.get_waiter('instance_running')
	waiter.wait(InstanceIds=[new_inst_id])
	assoc = dev_ec2_client.associate_address(
		AllocationId=eip_id,
		InstanceId=new_inst_id
    )
	if assoc["ResponseMetadata"]["HTTPStatusCode"] == 200:
		print("Allocated EIP successfully")
