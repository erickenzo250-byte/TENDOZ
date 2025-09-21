from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from . import models, database
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- USER ENDPOINTS ----------
@app.post("/users/")
def create_user(username: str, age: int, gender: str, bio: str, interests: str, db: Session = Depends(database.get_db)):
    user = models.User(username=username, age=age, gender=gender, bio=bio, interests=interests)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ---------- EXPLORE ----------
@app.get("/explore")
def explore(gender: str = None, min_age: int = 18, max_age: int = 100, interest: str = None, db: Session = Depends(database.get_db)):
    q = db.query(models.User).filter(models.User.age >= min_age, models.User.age <= max_age)
    if gender:
        q = q.filter(models.User.gender == gender)
    if interest:
        q = q.filter(models.User.interests.ilike(f"%{interest}%"))
    return q.all()

# ---------- LIKE & MATCH ----------
@app.post("/like/")
def like_user(liker_id: int, liked_id: int, db: Session = Depends(database.get_db)):
    like = models.Like(liker_id=liker_id, liked_id=liked_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    # check for match
    match = db.query(models.Like).filter_by(liker_id=liked_id, liked_id=liker_id).first()
    return {"liked": liked_id, "match": bool(match)}

# ---------- CHAT ----------
connections = {}

@app.websocket("/ws/{user_id}")
async def chat_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # Format: "receiver_id|message"
            receiver_id, msg = data.split("|", 1)
            receiver_id = int(receiver_id)

            # Save in DB
            db = next(database.get_db())
            message = models.Message(sender_id=user_id, receiver_id=receiver_id, content=msg)
            db.add(message)
            db.commit()

            if receiver_id in connections:
                await connections[receiver_id].send_text(f"{user_id}|{msg}")
    except:
        del connections[user_id]
