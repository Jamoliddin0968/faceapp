import multiprocessing as multi
import pickle
import time
from multiprocessing import Pool
from time import time

import dlib
import face_recognition
import MySQLdb
import numpy as np
import PIL
from decouple import config
from fastapi import BackgroundTasks
from sqlalchemy import text
from sqlalchemy.orm import Session
from tortoise.transactions import in_transaction

from src.config import IMAGE_DIR
from src.users.models import Encoding, User

face_detector = dlib.get_frontal_face_detector()


async def verify_picture(frame):
    img = face_recognition.load_image_file(frame.file)
    face_locations = face_detector(img)
    face_locations = [
        (rect.top(), rect.right(), rect.bottom(), rect.left())
        for rect in face_locations
    ]
    res = []
    for top, right, bottom, left in face_locations:
        res.append({"left": left, "top": top,
                   "right": right, "bottom": bottom})
    return res


async def verify_pickle(frame):
    img = pickle.loads(frame)
    face_locations = face_detector(img)
    face_locations = [
        (rect.top(), rect.right(), rect.bottom(), rect.left())
        for rect in face_locations
    ]
    res = []
    for top, right, bottom, left in face_locations:
        res.append({"left": left, "top": top,
                   "right": right, "bottom": bottom})
    return res


async def verify_frame(frame: bytes):
    frame = np.frombuffer(frame, dtype=np.uint8).reshape(480, 640, 3)
    face_locations = face_detector(frame)
    face_locations = [
        (rect.top(), rect.right(), rect.bottom(), rect.left())
        for rect in face_locations
    ]
    res = []
    for top, right, bottom, left in face_locations:
        res.append(
            {
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom,
            }
        )
    return res


def get_faces(db):
    data = db.query(Encoding).all()
    for face in data:
        frame = face.data

        frame = np.frombuffer(frame, dtype=np.uint8)

        face_locations = face_recognition.face_locations(frame)
        face_locations = [
            (rect.top(), rect.right(), rect.bottom(), rect.left())
            for rect in face_locations
        ]
        res = []
        for top, right, bottom, left in face_locations:
            res.append({"left": left, "top": top,
                       "right": right, "bottom": bottom})
        return res


async def face_detect(image, db: Session):
    face_encodings = db.query(Encoding).all()
    n = len(face_encodings)
    res = []
    known_face_enc = [None] * n
    known_face_id = [None] * n

    for enc in face_encodings:
        current_face = np.frombuffer(enc.data)
        known_face_enc[n - 1] = current_face
        known_face_id[n - 1] = enc.user_id
        n -= 1
    frame = face_recognition.load_image_file(image.file)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
        if len(face_encodings) > 0:
            matches = face_recognition.compare_faces(
                known_face_enc, face_encodings[0])
            try:
                match_index = matches.index(True)
                user_id = known_face_id[match_index]
                user = db.query(User).filter(User.id == user_id).first()
                res.append(
                    {
                        "name": user.name,
                        "left": left,
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                    }
                )
            except:
                pass
    return res


# dxfcgvhjkl;hgfdsjdgffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


async def face_detect2(image, db: Session):
    frame = np.array(PIL.Image.open(image.file))
    face_locations = face_detector(frame)
    a = time()
    face_encodings = db.execute(text("select user_id,data from encodings "))
    print(time() - a)
    res = []
    n = face_encodings.rowcount
    known_face_id = [False] * n
    known_face_enc = [False] * n
    for enc in face_encodings:
        n -= 1
        known_face_enc[n] = np.frombuffer(enc.data)
        known_face_id[n] = enc.user_id

    face_locations = [
        (rect.top(), rect.right(), rect.bottom(), rect.left())
        for rect in face_locations
    ]
    for top, right, bottom, left in face_locations:
        face_image = np.array(frame[top:bottom, left:right], dtype=np.uint8)
        face_encodings = face_recognition.face_encodings(face_image)
        if len(face_encodings) > 0:
            matches = face_recognition.compare_faces(
                known_face_enc, face_encodings[0])

            try:
                match_index = matches.index(True)
                user_id = known_face_id[match_index]
                user = db.execute(
                    text(f"select name from users where id={str(user_id)}")
                )
                if user:
                    res.append(
                        {
                            "name": user.first().name,
                            "left": left,
                            "top": top,
                            "right": right,
                            "bottom": bottom,
                        }
                    )
            except Exception as e:
                print(e.args)
    # print(time()-a)
    return res
