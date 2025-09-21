from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    bio = Column(Text, default="")
    interests = Column(Text, default="")
    profile_pic = Column(String, default="default.png")

    sent_likes = relationship("Like", back_populates="liker", foreign_keys="Like.liker_id")
    received_likes = relationship("Like", back_populates="liked", foreign_keys="Like.liked_id")

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey("users.id"))
    liked_id = Column(Integer, ForeignKey("users.id"))

    liker = relationship("User", back_populates="sent_likes", foreign_keys=[liker_id])
    liked = relationship("User", back_populates="received_likes", foreign_keys=[liked_id])

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    status = Column(String, default="sent")  # sent, delivered, read
