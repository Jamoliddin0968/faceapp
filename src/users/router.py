from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.database import get_db

from . import schema, services
from .models import User

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = services.get_users(db)
    return users


@router.post("/create/")
async def create_user(data: schema.User, db: Session = Depends(get_db)):
    obj = await services.create_user(data=data, db=db)
    return obj


@router.post("/{user_id}/upload_image/")
async def upload_image(
    user_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    obj = await services.upload_image(user_id=user_id, files=files, db=db)
    if obj:
        return {"msg": "ok"}
    raise HTTPException(status_code=400, detail="Hatolik yuz berdi")
