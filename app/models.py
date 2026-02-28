import uuid

from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict

from database import Model


class FileSchema(BaseModel):
    id: uuid.UUID
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class File(Model):
    __tablename__ = 'files'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
