from fastapi import UploadFile
from pydantic import BaseModel


class Data(BaseModel):
    image: UploadFile


class User(BaseModel):
    name: str = "username"
