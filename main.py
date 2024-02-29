import os

import ujson
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, UJSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import IMAGE_DIR
from src.database import get_db
from src.face.router import router as face_router
from src.users.models import User
from src.users.router import router as user_router

app = FastAPI()
os.makedirs(IMAGE_DIR, exist_ok=True)


@app.get("/hello")
def get_hello(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@app.get("/hello2")
def get_hello2(db: Session = Depends(get_db)):
    users = db.execute(text("select * from users"))
    r = [{"id": v.id, "name": v.name} for v in users]
    return UJSONResponse(content=r)


app.include_router(user_router)
app.include_router(face_router)

