import uuid

from fastapi import APIRouter, UploadFile, File

from storage import S3Storage
from settings import settings


router = APIRouter()


storage = S3Storage(
    bucket='tiny-cloud',
    endpoint=settings.endpoint,
    access_key=settings.access_key,
    secret_key=settings.secret_key
)


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    object_name = str(uuid.uuid4())
    await storage.upload(file, object_name)
    return {'file_id': object_name}


@router.get('/files/{file_id}')
async def get_file(file_id: str):
    url = await storage.get_object_link(file_id)
    return {'url': url}
