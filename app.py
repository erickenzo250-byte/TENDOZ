import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# ✅ Ensure tables exist on startup
Base.metadata.create_all(bind=engine)

# ✅ Seed demo users if none exist
def seed_users():
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        demo_users = [
            models.User(name="Alice", age=28, gender="Female", interests="Hiking, Reading"),
            models.User(name="Bob", age=32, gender="Male", interests="Music, Traveling"),
            models.User(name="Carol", age=25, gender="Female", interests="Cooking, Movies"),
        ]
        db.add_all(demo_users)
        db.commit()
    db.close()

seed_users()

# ---------------- STREAMLIT APP ---------------- #
st.set_page_config(page_title="💑 Dating Site", page_icon="💘", layout="wide")

st.title("💑 Browse Matches")

db = SessionLocal()
users = db.query(models.User).all()
db.close()

if users:
    for user in users:
        st.subheader(f"{user.name}, {user.age}")
        st.write(f"**Gender:** {user.gender}")
        st.write(f"**Interests:** {user.interests}")
        st.markdown("---")
else:
    st.warning("No users found. Add some profiles!")
