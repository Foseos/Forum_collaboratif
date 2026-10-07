"""Upload a local media backup to a public Neon Object Storage bucket."""

import argparse
import mimetypes
from pathlib import Path

import boto3
from botocore.config import Config


def read_env(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"').strip("'")
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--credentials", type=Path, required=True)
    parser.add_argument("--media", type=Path, required=True)
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args()

    env = read_env(args.credentials)
    required = ("AWS_ENDPOINT_URL_S3", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION")
    missing = [key for key in required if not env.get(key)]
    if missing:
        raise SystemExit("Paramètres manquants : " + ", ".join(missing))

    client = boto3.client(
        "s3",
        endpoint_url=env["AWS_ENDPOINT_URL_S3"],
        region_name=env["AWS_REGION"],
        aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"],
        config=Config(s3={"addressing_style": "path"}),
    )
    files = sorted(path for path in args.media.rglob("*") if path.is_file())
    for path in files:
        key = path.relative_to(args.media).as_posix()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        client.upload_file(str(path), args.bucket, key, ExtraArgs={"ContentType": content_type})
        client.head_object(Bucket=args.bucket, Key=key)
    print(f"Images transférées et vérifiées : {len(files)}")


if __name__ == "__main__":
    main()
