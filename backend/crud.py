from sqlalchemy.orm import Session
from . import models

def create_or_get_user(db: Session, username, age, gender, bio, interests, picture=""):
    user = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        user = models.User(username=username, age=age, gender=gender,
                           bio=bio, interests=interests, picture=picture)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_users(db: Session, exclude_id=None):
    query = db.query(models.User)
    if exclude_id:
        query = query.filter(models.User.id != exclude_id)
    return query.all()

def like_user(db: Session, liker_id, liked_id):
    exists = db.query(models.Like).filter_by(liker_id=liker_id, liked_id=liked_id).first()
    if not exists:
        db.add(models.Like(liker_id=liker_id, liked_id=liked_id))
        db.commit()

def get_matches(db: Session, user_id):
    likes_given = db.query(models.Like).filter_by(liker_id=user_id).all()
    matches = []
    for like in likes_given:
        reciprocal = db.query(models.Like).filter_by(liker_id=like.liked_id, liked_id=user_id).first()
        if reciprocal:
            matches.append(like.liked_id)
    return matches

def create_message(db: Session, chat_id, sender_id, receiver_id, content):
    msg = models.Message(chat_id=chat_id, sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, chat_id):
    return db.query(models.Message).filter(models.Message.chat_id==chat_id).order_by(models.Message.timestamp).all()
