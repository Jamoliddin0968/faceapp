from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    full_name = Column(String(50))

    encodings = relationship("Encoding", back_populates="user")


class Encoding(Base):
    __tablename__ = "encodings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(LargeBinary)
    image = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="encodings")
