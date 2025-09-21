import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import random

# ✅ Ensure tables exist
Base.metadata.create_all(bind=engine)

# Seed some demo users
def seed_users():
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        demo_users = [
            models.User(name="Alice", age=28, gender="Female",
                        interests="🌲 Hiking, 📚 Reading, ☕ Coffee",
                        avatar_url="https://i.pravatar.cc/150?img=5"),
            models.User(name="Bob", age=32, gender="Male",
                        interests="🎵 Music, ✈️ Traveling, ⚽ Football",
                        avatar_url="https://i.pravatar.cc/150?img=12"),
            models.User(name="Carol", age=25, gender="Female",
                        interests="🍳 Cooking, 🎬 Movies, 🧘 Yoga",
                        avatar_url="https://i.pravatar.cc/150?img=20"),
            models.User(name="David", age=30, gender="Male",
                        interests="🏋️ Gym, 🎮 Gaming, 🏍️ Motorbikes",
                        avatar_url="https://i.pravatar.cc/150?img=30"),
            models.User(name="Ella", age=27, gender="Female",
                        interests="🎨 Painting, 🎶 Dancing, 🌍 Exploring",
                        avatar_url="https://i.pravatar.cc/150?img=40"),
        ]
        db.add_all(demo_users)
        db.commit()
    db.close()

seed_users()

# ---------------- STREAMLIT APP ---------------- #
st.set_page_config(page_title="💘 Dating Site", page_icon="💘", layout="wide")

# Sidebar navigation
st.sidebar.title("💑 Dating App Menu")
page = st.sidebar.radio("Go to", ["Browse Profiles", "Matches ❤️", "Messages 💬", "Create Profile"])

db = SessionLocal()

# Simulate logged-in user (for demo)
current_user = db.query(models.User).first()

# ---------------- BROWSE PROFILES ---------------- #
if page == "Browse Profiles":
    st.title("💘 Browse Profiles")
    users = db.query(models.User).filter(models.User.id != current_user.id).all()

    if not users:
        st.info("No profiles available.")
    else:
        for user in users:
            st.markdown(
                f"""
                <div style="background-color:#fdf0f6;
                            border-radius:15px;
                            padding:20px;
                            margin-bottom:20px;
                            box-shadow:2px 2px 8px rgba(0,0,0,0.1);
                            text-align:center;">
                    <img src="{user.avatar_url}" style="width:120px;height:120px;border-radius:50%;margin-bottom:15px;">
                    <h3>{user.name}, {user.age}</h3>
                    <p><b>Gender:</b> {user.gender}</p>
                    <p><b>Interests:</b> {user.interests}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❤️ Like {user.name}", key=f"like_{user.id}"):
                    current_user.likes.append(user)
                    db.commit()
                    st.success(f"You liked {user.name}!")

            with col2:
                if st.button(f"❌ Pass {user.name}", key=f"pass_{user.id}"):
                    st.info(f"You passed on {user.name}")

# ---------------- MATCHES ---------------- #
elif page == "Matches ❤️":
    st.title("💖 Your Matches")
    matches = [u for u in current_user.likes if current_user in u.likes]

    if matches:
        for match in matches:
            st.markdown(
                f"""
                <div style="background:#e0ffe0;padding:15px;
                            margin-bottom:10px;border-radius:12px;">
                    <img src="{match.avatar_url}" style="width:80px;height:80px;border-radius:50%;float:left;margin-right:15px;">
                    <h4>{match.name}, {match.age}</h4>
                    <p>{match.interests}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No matches yet. Keep liking! ❤️")

# ---------------- MESSAGES ---------------- #
elif page == "Messages 💬":
    st.title("💬 Messages (Demo Only)")
    st.info("This is a placeholder chat system. Full chat requires a backend server.")

    matches = [u for u in current_user.likes if current_user in u.likes]
    if matches:
        match = st.selectbox("Select a match to chat with:", matches, format_func=lambda x: x.name)
        message = st.text_input(f"Send a message to {match.name}")
        if st.button("Send"):
            st.success(f"Message sent to {match.name}: {message}")
    else:
        st.warning("You have no matches to chat with.")

# ---------------- CREATE PROFILE ---------------- #
elif page == "Create Profile":
    st.title("➕ Create a New Profile")
    with st.form("create_profile"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=100, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        interests = st.text_area("Interests")
        avatar_choice = random.randint(1, 70)
        submitted = st.form_submit_button("Create Profile")

        if submitted and name:
            new_user = models.User(
                name=name,
                age=age,
                gender=gender,
                interests=interests,
                avatar_url=f"https://i.pravatar.cc/150?img={avatar_choice}",
            )
            db.add(new_user)
            db.commit()
            st.success(f"Profile created for {name}! 🎉")

db.close()
