import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_KEY")
AWS_REGION = "ap-southeast-2"
BUCKET_NAME = "suricata-rules-iitm"
FOLDER_PATH = "./rules"


# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_tar_files():
    # loop all files in the folder
    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".tar.gz"):
            local_file_path = os.path.join(FOLDER_PATH, file)
            s3_key = f"rules/{file}"   # path inside bucket

            print(f"Uploading {file} to s3://{BUCKET_NAME}/{s3_key} ...")

            try:
                s3.upload_file(local_file_path, BUCKET_NAME, s3_key)
                print(f"✔ Uploaded: {file}")
            except Exception as e:
                print(f"❌ Failed to upload {file}: {e}")

