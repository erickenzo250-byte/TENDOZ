import streamlit as st
from backend.database import SessionLocal, engine, Base
from backend import crud, models
import os

Base.metadata.create_all(bind=engine)
db = SessionLocal()

st.set_page_config(page_title="💖 Dating App", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["My Profile", "Explore", "Matches", "Chat"]
choice = st.sidebar.radio("Menu", menu)

# --- MY PROFILE ---
if choice == "My Profile":
    st.title("👤 My Profile")
    username = st.text_input("Username", "")
    age = st.number_input("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    bio = st.text_area("Bio")
    interests = st.text_input("Interests (comma separated)")

    # Optional: profile picture upload
    picture_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
    pic_filename = ""
    if picture_file:
        os.makedirs("assets", exist_ok=True)
        pic_filename = f"assets/{username}.png"
        with open(pic_filename, "wb") as f:
            f.write(picture_file.getbuffer())

    if st.button("Save / Login"):
        user = crud.create_or_get_user(db, username, age, gender, bio, interests, pic_filename)
        st.session_state.user = user
        st.success(f"Logged in as {user.username}")

# --- EXPLORE ---
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
                if u.picture and os.path.exists(u.picture):
                    st.image(u.picture, width=150)
                if st.button(f"Like {u.username}", key=f"like_{u.id}"):
                    crud.like_user(db, st.session_state.user.id, u.id)
                    st.success(f"You liked {u.username}!")
                st.markdown("---")

# --- MATCHES ---
elif choice == "Matches":
    st.title("❤️ Matches")
    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        matches_ids = crud.get_matches(db, st.session_state.user.id)
        matches = [db.query(models.User).get(mid) for mid in matches_ids]
        if not matches:
            st.info("No matches yet. Like users to find matches!")
        for u in matches:
            st.subheader(f"{u.username} ({u.age}, {u.gender})")
            st.write(f"💬 {u.bio}")
            st.write(f"✨ Interests: {u.interests}")
            if u.picture and os.path.exists(u.picture):
                st.image(u.picture, width=150)
            st.markdown("---")

# --- CHAT ---
elif choice == "Chat":
    st.title("💬 Chat")
    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        matches_ids = crud.get_matches(db, st.session_state.user.id)
        if not matches_ids:
            st.info("No matches to chat with yet.")
        else:
            matches = [db.query(models.User).get(mid) for mid in matches_ids]
            partner = st.selectbox("Choose someone to chat with", [u.username for u in matches])
            partner_user = next(u for u in matches if u.username == partner)
            chat_id = f"{min(st.session_state.user.id, partner_user.id)}-{max(st.session_state.user.id, partner_user.id)}"

            # Show messages
            messages = crud.get_messages(db, chat_id)
            for m in messages:
                sender = "You" if m.sender_id == st.session_state.user.id else partner_user.username
                st.write(f"**{sender}**: {m.content} ({m.timestamp})")

            msg = st.text_input("Type a message", key="msg_input")
            if st.button("Send"):
                if msg.strip() != "":
                    crud.create_message(db, chat_id, st.session_state.user.id, partner_user.id, msg)
                    st.experimental_rerun()
