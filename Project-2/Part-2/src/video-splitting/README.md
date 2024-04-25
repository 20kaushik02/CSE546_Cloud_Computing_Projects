# Stage 1: video splitting

- `handler.py` gets the uploaded video file, splits a frame using `ffmpeg`, uploads the output frame to another bucket
- then it asynchronously invokes the lambda function for stage 2
- `stage1_policy.json` defines the permission policy needed for the lambda function's IAM role
- `dummy_s3_trigger_event.json` is a sample S3 PUT event
