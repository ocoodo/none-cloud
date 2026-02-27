import aioboto3
from fastapi import UploadFile


class S3Storage:
    def __init__(self, 
        bucket: str, 
        endpoint: str, 
        access_key: str, 
        secret_key: str
    ):
        self.bucket = bucket
        self.endpoint = endpoint
        self.session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
    async def upload(self, file: UploadFile, object_name: str):
        async with self.session.client('s3', endpoint_url=self.endpoint) as s3:
            await s3.upload_fileobj(
                file.file,
                self.bucket,
                object_name,
                ExtraArgs={
                    'ContentType': file.content_type
                }
            )
    
    async def get_object_link(
        self, 
        object_name: str, 
        expires_in: int = 15 * 60
    ):
        async with self.session.client('s3', endpoint_url=self.endpoint) as s3:
            url = await s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': object_name
                },
                ExpiresIn=expires_in
            )
        return url
    