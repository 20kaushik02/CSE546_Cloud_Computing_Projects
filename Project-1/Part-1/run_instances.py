import boto3

# creds from ~/.aws/credentials
session = boto3.Session(profile_name="dev")
dev_ec2_client = session.client("ec2", region_name="us-east-1")

# Create capacity reservation of instances
ami_id = "ami-0c7217cdde317cfec" # Ubuntu Server 22.04 LTS, SSD on EBS, 64-bit (x86)
reservation = dev_ec2_client.run_instances(
    ImageId=ami_id,
	KeyName='cse546-dev',
    MinCount=1,  # if available instances are less than min_count, abort with no allocation
    MaxCount=1,  # try to allocate max_count instances. we only need one for now
    InstanceType="t2.micro",
    TagSpecifications=[
        {"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": "WebTier"}]}
    ],
)

print("Instances allocated successfully:", "Yes" if reservation else "No")
print("Groups:", len(reservation["Groups"])) # TODO: add grp info logging
print("Instances:", len(reservation["Instances"]))
for inst_idx, inst in enumerate(reservation["Instances"]):
	print("Instance", inst_idx + 1, ":-")
	print("\tInstance ID:", inst["InstanceId"])
	print("\tInstance state:", inst["State"]["Name"])
	print(f"\t{inst["InstanceType"]} in {inst["Placement"]["AvailabilityZone"]}")
	print(f"\t{inst["CpuOptions"]["CoreCount"]}vCPU, {inst["Hypervisor"]} hypervisor")
