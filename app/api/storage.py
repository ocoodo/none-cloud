import uuid
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile
from sqlalchemy import select

from database import DbSession
from storage import S3Storage
from settings import settings
from models import File, FileSchema


router = APIRouter()


storage = S3Storage(
    bucket='tiny-cloud',
    endpoint=settings.endpoint,
    access_key=settings.access_key,
    secret_key=settings.secret_key
)


@router.post('/upload')
async def upload(
    db_session: DbSession,
    file: UploadFile
):
    file_id = uuid.uuid4()
    original_name = file.filename
    
    await storage.upload(file, str(file_id))
    
    file = File(
        id=file_id,
        name=original_name
    )
    db_session.add(file)
    await db_session.commit()
    
    return {'file_id': file.id}


@router.get(
    '/files',
    response_model=List[FileSchema]
)
async def get_files_list(db_session: DbSession):
    query = await db_session.execute(select(File))
    files = query.scalars().all()
    return files
    """
    return [
        {
            'id': str(file.id),
            'name': file.name
        } for file in files
    ]"""


@router.get('/files/{file_id}')
async def get_file(
    db_session: DbSession,
    file_id: uuid.UUID
):
    query = await db_session.execute(
        select(File)
        .where(File.id == file_id)
    )
    file = query.scalar_one_or_none()
    if not file:
        raise HTTPException(
            status_code=404,
            detail='File not found'
        )
    url = await storage.get_object_link(str(file.id), file.name)
    return {'url': url}
