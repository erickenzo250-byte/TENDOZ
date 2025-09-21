import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import os

# ✅ Ensure tables exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    st.error(f"Error creating tables: {e}")

# ✅ Seed demo users if none exist
def seed_users():
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            demo_users = [
                models.User(name="Alice", age=28, gender="Female", interests="Hiking, Reading"),
                models.User(name="Bob", age=32, gender="Male", interests="Music, Traveling"),
                models.User(name="Carol", age=25, gender="Female", interests="Cooking, Movies"),
            ]
            db.add_all(demo_users)
            db.commit()
    except Exception as e:
        st.error(f"Error seeding users: {e}")
    finally:
        db.close()

seed_users()

# ---------------- STREAMLIT APP ---------------- #
st.set_page_config(page_title="💑 Dating Site", page_icon="💘", layout="wide")

st.title("💑 Browse Matches")

# Debug info (optional - can remove later)
st.caption(f"Database Path: {os.path.abspath('dating.db')}")

db = SessionLocal()
users = []
try:
    users = db.query(models.User).all()
except Exception as e:
    st.error(f"Database error: {e}")
finally:
    db.close()

if users:
    for user in users:
        st.subheader(f"{user.name}, {user.age}")
        st.write(f"**Gender:** {user.gender}")
        st.write(f"**Interests:** {user.interests}")
        st.markdown("---")
else:
    st.warning("No users found. Add some profiles!")

# ✅ Add new user form
with st.form("add_user_form"):
    st.subheader("➕ Add a New Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    interests = st.text_area("Interests (comma separated)")
    submitted = st.form_submit_button("Add Profile")

    if submitted and name:
        db = SessionLocal()
        new_user = models.User(name=name, age=age, gender=gender, interests=interests)
        db.add(new_user)
        db.commit()
        db.close()
        st.success(f"✅ Profile for {name} added! Refresh to see it.")
