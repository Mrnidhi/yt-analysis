import boto3
import io
import csv
import re
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def clean_column_name(name):
    return re.sub(r'\W+', '_', name.strip().lower())

def lambda_handler(event, context):
    try:
        logger.info(f"🚀 Lambda started. Event: {json.dumps(event)}")

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        if not key.endswith('.csv') or 'raw/' not in key:
            logger.warning(f"⚠️ Skipping file: {key}")
            return {'statusCode': 200, 'body': 'Not a valid input file'}

        logger.info(f"📥 Reading file from: s3://{bucket}/{key}")

        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_body = obj['Body'].read().decode('utf-8')
        reader = csv.reader(io.StringIO(csv_body))

        rows = list(reader)
        if not rows:
            raise ValueError("CSV file is empty")

        header = [clean_column_name(col) for col in rows[0]]
        data = rows[1:]

        output_buffer = io.StringIO()
        writer = csv.writer(output_buffer)
        writer.writerow(header)
        writer.writerows(data)

        clean_key = key.replace("raw/", "clean/")
        s3.put_object(Bucket=bucket, Key=clean_key, Body=output_buffer.getvalue())

        logger.info(f"✅ Cleaned file written to: s3://{bucket}/{clean_key}")

        return {
            'statusCode': 200,
            'body': f"Cleaned file saved to: s3://{bucket}/{clean_key}"
        }

    except Exception as e:
        logger.error("❌ Error in processing", exc_info=True)
        return {
            'statusCode': 500,
            'body': str(e)
        }
