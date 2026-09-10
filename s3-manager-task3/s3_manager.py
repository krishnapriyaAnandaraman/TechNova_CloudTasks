"""
S3 File Manager
----------------
Simple CLI tool to upload, download, list, and delete files in an S3 bucket,
with optional metadata tagging.

Setup:
    pip install boto3
    aws configure   # or set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION

Usage:
    python s3_manager.py upload <local_path> <bucket> <key> [--meta key=value ...]
    python s3_manager.py download <bucket> <key> <local_path>
    python s3_manager.py list <bucket> [--prefix some/path/]
    python s3_manager.py delete <bucket> <key>
    python s3_manager.py metadata <bucket> <key>
"""

import argparse
import sys

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

s3 = boto3.client("s3")


def upload_file(local_path, bucket, key, metadata=None):
    extra_args = {"Metadata": metadata} if metadata else None
    try:
        if extra_args:
            s3.upload_file(local_path, bucket, key, ExtraArgs=extra_args)
        else:
            s3.upload_file(local_path, bucket, key)
        print(f"Uploaded '{local_path}' to 's3://{bucket}/{key}'")
    except FileNotFoundError:
        print(f"Error: local file '{local_path}' not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found. Run 'aws configure' first.")
    except ClientError as e:
        print(f"Error uploading file: {e}")


def download_file(bucket, key, local_path):
    try:
        s3.download_file(bucket, key, local_path)
        print(f"Downloaded 's3://{bucket}/{key}' to '{local_path}'")
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Error: '{key}' not found in bucket '{bucket}'.")
        else:
            print(f"Error downloading file: {e}")


def list_files(bucket, prefix=""):
    try:
        paginator = s3.get_paginator("list_objects_v2")
        found_any = False
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                found_any = True
                size_kb = obj["Size"] / 1024
                print(f"  {obj['Key']:<50} {size_kb:>8.1f} KB   {obj['LastModified']}")
        if not found_any:
            print(f"No files found in bucket '{bucket}' (prefix='{prefix}').")
    except ClientError as e:
        print(f"Error listing files: {e}")


def delete_file(bucket, key):
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Deleted 's3://{bucket}/{key}'")
    except ClientError as e:
        print(f"Error deleting file: {e}")


def get_metadata(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        metadata = response.get("Metadata", {})
        if metadata:
            print(f"Metadata for '{key}':")
            for k, v in metadata.items():
                print(f"  {k}: {v}")
        else:
            print(f"No custom metadata set on '{key}'.")
    except ClientError as e:
        print(f"Error fetching metadata: {e}")


def parse_metadata_args(meta_args):
    metadata = {}
    if meta_args:
        for pair in meta_args:
            if "=" not in pair:
                print(f"Skipping malformed --meta value '{pair}' (expected key=value)")
                continue
            k, v = pair.split("=", 1)
            metadata[k] = v
    return metadata


def main():
    parser = argparse.ArgumentParser(description="Simple S3 file manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_upload = sub.add_parser("upload")
    p_upload.add_argument("local_path")
    p_upload.add_argument("bucket")
    p_upload.add_argument("key")
    p_upload.add_argument("--meta", action="append", help="key=value, repeatable")

    p_download = sub.add_parser("download")
    p_download.add_argument("bucket")
    p_download.add_argument("key")
    p_download.add_argument("local_path")

    p_list = sub.add_parser("list")
    p_list.add_argument("bucket")
    p_list.add_argument("--prefix", default="")

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("bucket")
    p_delete.add_argument("key")

    p_meta = sub.add_parser("metadata")
    p_meta.add_argument("bucket")
    p_meta.add_argument("key")

    args = parser.parse_args()

    if args.command == "upload":
        metadata = parse_metadata_args(args.meta)
        upload_file(args.local_path, args.bucket, args.key, metadata)
    elif args.command == "download":
        download_file(args.bucket, args.key, args.local_path)
    elif args.command == "list":
        list_files(args.bucket, args.prefix)
    elif args.command == "delete":
        delete_file(args.bucket, args.key)
    elif args.command == "metadata":
        get_metadata(args.bucket, args.key)


if __name__ == "__main__":
    main()
