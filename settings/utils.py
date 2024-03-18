import json
import io
import boto3


def download_s3(
    *,
    file: str,
    aws_storage_bucket_name: str
):
    name_bucket = aws_storage_bucket_name
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=name_bucket, Key=file)
        content = response['Body'].read()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error al descargar el archivo desde S3: {str(e)}")
        return None


def save_content_s3(
    *,
    content: dict,
    name_file: str,
    aws_storage_bucket_name: str
):
    """
    Guardar un dict a s3 directamente
    """
    name_bucket = aws_storage_bucket_name
    s3 = boto3.client('s3')
    json_data = json.dumps(content)
    try:
        s3.put_object(Bucket=name_bucket, Key=name_file, Body=json_data)
        url_objeto_s3 = f"https://{name_bucket}.s3.amazonaws.com/{name_file}"
        return url_objeto_s3
    except Exception as e:
        print(f"Error al subir el archivo a S3: {str(e)}")
        return None
