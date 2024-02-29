import os
import time

import face_recognition
import ujson
from fastapi import Depends, HTTPException
from fastapi.responses import UJSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import IMAGE_DIR
from src.database import get_db

from .models import Encoding, User


def get_users(db: Session):
    rows = db.execute(text("select * from users")).all()
    return rows


async def create_user(data, db):
    user = db.query(User).filter(User.name == data.name).first()
    if not user:
        user = User(name=data.name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


async def upload_image(user_id, files, db):
    objects = []
    if files:
        for image in files:
            current_time = time.time()
            current_time_int = int(current_time)
            ext = image.filename.split(".")[-1]
            img_path = os.path.join(IMAGE_DIR, f"{current_time_int}.{ext}")
            with open(img_path, "wb") as f:
                f.write(image.file.read())
            face = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(face)
            if len(face_bounding_boxes) > 0:
                face_enc = face_recognition.face_encodings(face)[0]
                objects.append(
                    Encoding(image=img_path, data=face_enc.tobytes(), user_id=user_id)
                )
        if len(objects) > 0:
            db.add_all(objects)
            db.commit()
    return True
