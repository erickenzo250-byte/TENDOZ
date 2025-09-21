from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    bio = Column(String, default="")
    interests = Column(String, default="")
    picture = Column(String, default="")  # store image filename

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    liker_id = Column(Integer, ForeignKey("users.id"))
    liked_id = Column(Integer, ForeignKey("users.id"))

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    read = Column(Boolean, default=False)
