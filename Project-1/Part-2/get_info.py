import boto3
from pprint import pprint

# creds from ~/.aws/credentials
session = boto3.Session(profile_name="dev")

region1="us-east-1"
dev_ec2_client = session.client("ec2", region_name=region1)
dev_s3_client = session.client("s3", region_name=region1)
dev_sqs_client = session.client("sqs", region_name=region1)

# Get all instances' information
all_instances = dev_ec2_client.describe_instances()
with open("output.txt", "w") as out_f:
	pprint(all_instances, stream=out_f)

print("Capacity Reservations:", len(all_instances["Reservations"]))
for idx, reservation in enumerate(all_instances["Reservations"]):
    print("Reservation", idx + 1, ":-")
    print("\tGroups:", len(reservation["Groups"])) # TODO: add grp info logging
    print("\tInstances:", len(reservation["Instances"]))
    for inst_idx, instance in enumerate(reservation["Instances"]):
        print("\tInstance", inst_idx + 1, ":-")
        print("\t\tInstance ID:", instance["InstanceId"])
        print("\t\tInstance state:", instance["State"]["Name"])
        print(f"\t\t{instance["InstanceType"]} in {instance["Placement"]["AvailabilityZone"]}")
        print(f"\t\t{instance["CpuOptions"]["CoreCount"]}vCPU, {instance["Hypervisor"]} hypervisor")
        print(f"\t\t{instance["PlatformDetails"]} on {instance["RootDeviceType"]} volume")
        print("\t\tPublic IP address:", instance["PublicIpAddress"] if "PublicIpAddress" in instance else "N/A")

# Get all buckets' information
all_buckets = dev_s3_client.list_buckets()
with open("output.txt", "a") as out_f:
	pprint(all_buckets, stream=out_f)

print("Buckets:", len(all_buckets["Buckets"]))
for bucket in all_buckets["Buckets"]:
    print("\tName:", bucket["Name"])

# Get all queues' information
all_queues = dev_sqs_client.list_queues()
with open("output.txt", "a") as out_f:
	pprint(all_queues, stream=out_f)

print("Queues:", len(all_queues["QueueUrls"]))
for queue in all_queues["QueueUrls"]:
    print("\tQueue URL:", queue)
