from sqlalchemy.orm import Session
from . import models

def get_or_create_user(db: Session, username: str, age: int, gender: str, bio: str, interests: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        user = models.User(username=username, age=age, gender=gender, bio=bio, interests=interests)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_users(db: Session, exclude_id: int = None):
    query = db.query(models.User)
    if exclude_id:
        query = query.filter(models.User.id != exclude_id)
    return query.all()

def create_message(db: Session, chat_id: str, sender_id: int, receiver_id: int, content: str):
    msg = models.Message(chat_id=chat_id, sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, chat_id: str):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.timestamp).all()
