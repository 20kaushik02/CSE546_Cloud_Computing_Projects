import json
import urllib.parse
import boto3
from video_splitting_cmdline import video_splitting_cmdline

print("Loading function")

# attach execution policies and IAM roles in deployment lambda
sesh = boto3.Session()

s3_client = sesh.client("s3", region_name="us-east-1")
lambda_client = sesh.client("lambda", region_name="us-east-1")


def handler(event, context):
    for record in event["Records"]:
        # get uploaded object
        in_bucket = record["s3"]["bucket"]["name"]
        if in_bucket != "1229569564-input":
            continue
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"], encoding="utf-8")
        tmpkey = key.replace("/", "")
        download_path = "/tmp/{}".format(tmpkey)
        s3_client.download_file(in_bucket, key, download_path)

        # process it
        out_file = video_splitting_cmdline(download_path)

        # upload output object
        s3_client.upload_file(
            "/tmp/" + out_file,
            "1229569564-stage-1",
            out_file,
        )

        # invoke face recognition lambda
        # https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html
        # (note: better to use SNS or some dedicated event handling mechanism rather than direct invocation?)
        invocation_params = {
            "bucket_name": "1229569564-stage-1",
            "image_file_name": out_file,
        }

        invoke_response = lambda_client.invoke(
            FunctionName="face-recognition",
            InvocationType="Event",
            Payload=json.dumps(invocation_params),
        )
        print(invoke_response)
    return


if __name__ == "__main__":
    with open("dummy_s3_trigger_event.json", "r") as dummy_event:
        event = json.loads(dummy_event.read())
    handler(event, None)
