import streamlit as st
from backend.database import SessionLocal, engine, Base
from backend import crud, models

# Create DB tables
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="💖 Dating App", layout="wide")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# Tabs
menu = ["My Profile", "Explore", "Chat"]
choice = st.sidebar.selectbox("Menu", menu)

db = SessionLocal()

# --- My Profile ---
if choice == "My Profile":
    st.title("👤 My Profile")
    username = st.text_input("Username", "")
    age = st.number_input("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    bio = st.text_area("Bio")
    interests = st.text_input("Interests (comma separated)")

    if st.button("Save / Login"):
        user = crud.get_or_create_user(db, username, age, gender, bio, interests)
        st.session_state.user = user
        st.success(f"Logged in as {user.username}")

# --- Explore ---
elif choice == "Explore":
    st.title("🌍 Explore Profiles")
    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        users = crud.get_users(db, exclude_id=st.session_state.user.id)
        for u in users:
            with st.container():
                st.subheader(f"{u.username} ({u.age}, {u.gender})")
                st.write(f"💬 {u.bio}")
                st.write(f"✨ Interests: {u.interests}")
                st.markdown("---")

# --- Chat ---
elif choice == "Chat":
    st.title("💬 Chat")
    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        users = crud.get_users(db, exclude_id=st.session_state.user.id)
        partner = st.selectbox("Choose someone to chat with", [u.username for u in users] if users else [])
        if partner:
            partner_user = [u for u in users if u.username == partner][0]
            chat_id = f"{min(st.session_state.user.id, partner_user.id)}-{max(st.session_state.user.id, partner_user.id)}"

            # Messages
            messages = crud.get_messages(db, chat_id)
            for m in messages:
                sender = "You" if m.sender_id == st.session_state.user.id else partner_user.username
                st.write(f"**{sender}**: {m.content} ({m.timestamp})")

            # New message
            msg = st.text_input("Type a message")
            if st.button("Send"):
                crud.create_message(db, chat_id, st.session_state.user.id, partner_user.id, msg)
                st.experimental_rerun()
