from backend.database import SessionLocal, Base, engine
from backend import models
import os

# Create database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Sample users
sample_users = [
    {"username":"alice","age":25,"gender":"Female","bio":"Love music and art! 🎨🎶","interests":"🎵 Music, 🎨 Art","picture":"assets/alice.png"},
    {"username":"bob","age":28,"gender":"Male","bio":"Sports fan and foodie! ⚽🍔","interests":"⚽ Soccer, 🍔 Food","picture":"assets/bob.png"},
    {"username":"carol","age":23,"gender":"Female","bio":"Traveler and reader 🌍📚","interests":"🌍 Travel, 📚 Reading","picture":"assets/carol.png"},
    {"username":"dave","age":30,"gender":"Male","bio":"Gaming geek 🎮","interests":"🎮 Gaming, 🏀 Basketball","picture":"assets/dave.png"}
]

for u in sample_users:
    user = models.User(**u)
    db.add(user)

db.commit()
print("Database created and sample users added.")
