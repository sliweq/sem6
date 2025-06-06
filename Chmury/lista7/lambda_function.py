import json
import qrcode
import boto3
import os
import uuid
from io import BytesIO
from urllib.parse import urlparse

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'qr-code-bucket-sliweq')
REGION = os.environ.get('AWS_REGION', 'us-east-1') 

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        url = body.get('url')
        if not url or not urlparse(url).scheme:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid URL'})
            }

        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)

        filename = f"{uuid.uuid4()}.png"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=buffer,
            ContentType='image/png',
        )

        public_url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}"

        return {
            'statusCode': 200,
            'body': json.dumps({'qr_code_url': public_url})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
