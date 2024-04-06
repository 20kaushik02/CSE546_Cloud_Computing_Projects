# Part-1: Video-splitting stage - S3-triggered Lambda

- `handler.py` gets the uploaded video file, splits 10 frames using `ffmpeg`, uploads the output folder of frames to another bucket
- `lambda_s3_policy.json` defines the permission policy needed for the lambda function's IAM role
- `dummy_s3_trigger_event.json` is a sample S3 PUT event
