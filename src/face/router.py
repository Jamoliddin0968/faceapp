# import base64
import json
from typing import Annotated, List

import numpy as np
import PIL
from fastapi import (APIRouter, BackgroundTasks, Depends, File, Form,
                     HTTPException, UploadFile)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import get_db

from . import schemas, services

router = APIRouter(prefix="/face")


@router.post("/")
async def get_face(frame: UploadFile, db: Session = Depends(get_db)):
    res = await services.verify_picture(frame)
    return JSONResponse(res)


@router.post("/all/")
async def get_faces(db: Session = Depends(get_db)):
    res = services.get_faces(db)
    return JSONResponse(res)


@router.post("/bytes/")
async def get_face(fbytes: Annotated[bytes, File()], db: Session = Depends(get_db)):
    res = await services.verify_frame(fbytes)
    return JSONResponse(res)


@router.post("/pickle/")
async def get_face(task: BackgroundTasks,frame: Annotated[bytes, File()], db: Session = Depends(get_db)):
    task.add_task(services.verify_pickle,frame)
    return []


@router.post("/detect/")
async def face_detect(task: BackgroundTasks, image: UploadFile, db: Session = Depends(get_db)):
    res = await services.face_detect(image=image, db=db)
    return res


@router.post("/detect_test_method/")
async def face_detect2(image: UploadFile, db: Session = Depends(get_db)):
    res = await services.face_detect2(image=image, db=db)
    return res
