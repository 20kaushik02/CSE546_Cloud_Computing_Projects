import os
import json
import boto3
from face_recognition_code import face_recognition_function

print("Loading function")

# attach execution policies and IAM roles in deployment lambda
sesh = boto3.Session()

s3_client = sesh.client("s3", region_name="us-east-1")

def handler(event, context):
    # get processed object from event info
    image = event["image_file_name"]
    in_bucket = event["bucket_name"]
    download_path = "/tmp/" + image
    s3_client.download_file(in_bucket, image, download_path)

    # process it
    face_output = face_recognition_function(download_path)

    # upload output object
    if face_output is not None:
        key = os.path.splitext(image)[0]
        s3_client.upload_file("/tmp/" + key + ".txt", "1229569564-output", key + ".txt")
        return 0
    else:
        return 1


if __name__ == "__main__":
    with open("dummy_lambda_invocation_event.json", "r") as dummy_event:
        event = json.loads(dummy_event.read())
    handler(event, None)
