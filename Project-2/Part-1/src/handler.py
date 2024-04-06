import os
import subprocess
import json
import urllib.parse
import boto3

print("Loading function")


# attach execution policies and IAM roles in deployment lambda
sesh = boto3.Session()

s3 = sesh.client("s3", region_name="us-east-1")


def video_splitting_cmdline(video_filename):
    filename = os.path.basename(video_filename)
    outdir = os.path.splitext(filename)[0]
    outdir = os.path.join("/tmp", outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    split_cmd = (
        "ffmpeg -ss 0 -r 1 -i "
        + video_filename
        + " -vf fps=1/1 -start_number 0 -vframes 10 "
        + outdir
        + "/"
        + "output-%02d.jpg -y"
    )
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    return outdir


def handler(event, context):
    for record in event["Records"]:
        # get uploaded object
        in_bucket = record["s3"]["bucket"]["name"]
        if in_bucket != "1229569564-input":
            continue
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"], encoding="utf-8")
        tmpkey = key.replace("/", "")
        download_path = "/tmp/{}".format(tmpkey)
        s3.download_file(in_bucket, key, download_path)

        # process it
        out_dir = video_splitting_cmdline(download_path)

        # upload output objects
        for frame in os.listdir(out_dir):
            s3.upload_file(
                os.path.join(out_dir, frame),
                "1229569564-stage-1",
                os.path.splitext(tmpkey)[0] + "/" + frame,
            )


if __name__ == "__main__":
    with open("dummy_s3_trigger_event.json", "r") as dummy_event:
        event = json.loads(dummy_event.read())
    handler(event, None)
