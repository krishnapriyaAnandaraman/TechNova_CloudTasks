# S3 File Manager

## 1. AWS setup (one-time)
1. Sign up for an [AWS Free Tier](https://aws.amazon.com/free/) account (requires a card, but S3 at this
   scale stays within the free tier: 5 GB storage, 20,000 GET / 2,000 PUT requests per month).
2. In the AWS Console, go to **S3** → **Create bucket**. Give it a globally unique name
   (e.g. `kicchu-file-manager-demo`) and leave other settings default.
3. Go to **IAM** → **Users** → **Create user**. Give it **programmatic access** and attach the
   `AmazonS3FullAccess` policy (or a scoped-down custom policy for just your bucket, if you want
   to be stricter).
4. Save the generated **Access Key ID** and **Secret Access Key** — you won't see the secret again.

## 2. Configure your machine
```bash
pip install boto3
aws configure
# AWS Access Key ID: <paste>
# AWS Secret Access Key: <paste>
# Default region name: ap-south-1   (or whichever region your bucket is in)
# Default output format: json
```
(If you don't have the `aws` CLI installed, you can instead set environment variables
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` — boto3 will pick them up.)

## 3. Usage
```bash
# Upload a file
python s3_manager.py upload ./notes.txt my-bucket-name notes.txt

# Upload with metadata tags (bonus)
python s3_manager.py upload ./notes.txt my-bucket-name notes.txt --meta uploaded-by=kicchu --meta category=demo

# List all files in the bucket
python s3_manager.py list my-bucket-name

# List files under a prefix (like a folder)
python s3_manager.py list my-bucket-name --prefix docs/

# Download a file
python s3_manager.py download my-bucket-name notes.txt ./downloaded_notes.txt

# View metadata on a file
python s3_manager.py metadata my-bucket-name notes.txt

# Delete a file
python s3_manager.py delete my-bucket-name notes.txt
```

## Troubleshooting
- **`NoCredentialsError`** — `aws configure` wasn't run, or the credentials file is empty. Re-run step 2.
- **`AccessDenied`** — the IAM user's policy doesn't cover the action or bucket; check the policy attached in step 3.
- **`404` on download** — the key (filename) doesn't match exactly what's in the bucket; run `list` first to confirm the exact key.
- **Bucket name errors on creation** — S3 bucket names are globally unique across *all* AWS accounts; add a personal suffix like `-kicchu-2026`.
