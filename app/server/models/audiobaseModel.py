from pydantic import BaseModel, Field, BaseSettings
from uuid import uuid4
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List, Annotated
from datetime import datetime, date


class Song(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    name: str = Field(..., exclusiveMaximum=10)
    duration: int = Field(...)
    uploaded_time: datetime = Field(...)

class Podcast(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    name: str = Field(..., exclusiveMaximum=10)
    duration: int = Field(...)
    uploaded_time: datetime = Field(...)
    host: str = Field(...)
    participants:str= Field([str], exclusiveMaximum=10)


class AudioBook(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    title: str = Field(...)
    author: str = Field(..., exclusiveMaximum=100)
    narrator: str = Field(..., exclusiveMaximum=100)
    duration: int = Field(...)
    uploaded_time: datetime = Field(...)


class AudioFileType(BaseModel):
    Song
    Podcast
    AudioBook

class audioFileMetadata(BaseModel):
    # id: PyObjectId = Field(alias='_id')
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    metadata :str

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}