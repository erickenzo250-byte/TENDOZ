import streamlit as st
from backend.database import SessionLocal, engine, Base
from backend import crud, models
import os

# Initialize DB
Base.metadata.create_all(bind=engine)
db = SessionLocal()

st.set_page_config(page_title="💖 Dating App", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["My Profile", "Explore", "Matches", "Chat"]
choice = st.sidebar.radio("Menu", menu)

# CSS for cards, badges, chat bubbles
st.markdown("""
<style>
body {background: linear-gradient(120deg, #fdfbfb, #ebedee);}
.card {border-radius: 15px; padding: 10px; margin-bottom: 15px; background-color:#fff0f5; box-shadow:0 4px 8px rgba(0,0,0,0.2);}
.badge {background:#ffeb3b; padding:3px 8px; border-radius:10px; margin:2px;}
.chat-you {background:#c1f0c1;padding:8px;margin:3px;border-radius:12px;text-align:right;}
.chat-partner {background:#f0c1c1;padding:8px;margin:3px;border-radius:12px;text-align:left;}
button.stButton > button:hover {background: #ff4081; color:white;}
</style>
""", unsafe_allow_html=True)

# --- MY PROFILE ---
if choice == "My Profile":
    st.title("👤 My Profile")
    username = st.text_input("Username", "")
    age = st.number_input("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    bio = st.text_area("Bio", placeholder="Write something fun about yourself!")
    interests = st.text_input("Interests (comma separated)", placeholder="🎵 Music, 🏀 Sports, 🎮 Gaming")

    picture_file = st.file_uploader("Upload Profile Picture", type=["png","jpg","jpeg"])
    pic_filename = ""
    if picture_file:
        os.makedirs("assets", exist_ok=True)
        pic_filename = f"assets/{username}.png"
        with open(pic_filename, "wb") as f:
            f.write(picture_file.getbuffer())

    if st.button("Save / Login"):
        user = crud.create_or_get_user(db, username, age, gender, bio, interests, pic_filename)
        st.session_state.user = user
        st.toast(f"Welcome {user.username}! 🎉")

# --- EXPLORE ---
elif choice == "Explore":
    st.title("🌍 Explore Profiles")
    if not st.session_state.user:
        st.warning("Please log in first.")
    else:
        users = crud.get_users(db, exclude_id=st.session_state.user.id)
        for u in users:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            cols = st.columns([1,2])
            with cols[0]:
                st.image(u.picture if u.picture and os.path.exists(u.picture) else "https://via.placeholder.com/80", width=80)
            with cols[1]:
                st.subheader(f"{u.username} ({u.age})")
                st.write(f"💬 {u.bio}")
                badges = "".join([f'<span class="badge">{i.strip()}</span>' for i in u.interests.split(",")])
                st.markdown(badges, unsafe_allow_html=True)
                if st.button(f"❤️ Like {u.username}", key=f"like_{u.id}"):
                    crud.like_user(db, st.session_state.user.id, u.id)
                    st.toast(f"You liked {u.username}!")
            st.markdown("</div>", unsafe_allow_html=True)

# --- MATCHES ---
elif choice == "Matches":
    st.title("❤️ Matches")
    if not st.session_state.user:
        st.warning("Please log in first.")
    else:
        matches_ids = crud.get_matches(db, st.session_state.user.id)
        matches = [db.query(models.User).get(mid) for mid in matches_ids]
        if not matches:
            st.info("No matches yet. Like users to find matches!")
        for u in matches:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            cols = st.columns([1,2])
            with cols[0]:
                st.image(u.picture if u.picture and os.path.exists(u.picture) else "https://via.placeholder.com/80", width=80)
            with cols[1]:
                st.subheader(f"{u.username} ({u.age})")
                st.write(f"💬 {u.bio}")
                badges = "".join([f'<span class="badge">{i.strip()}</span>' for i in u.interests.split(",")])
                st.markdown(badges, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- CHAT ---
elif choice == "Chat":
    st.title("💬 Chat")
    if not st.session_state.user:
        st.warning("Please log in first.")
    else:
        matches_ids = crud.get_matches(db, st.session_state.user.id)
        if not matches_ids:
            st.info("No matches to chat with yet.")
        else:
            matches = [db.query(models.User).get(mid) for mid in matches_ids]
            partner = st.selectbox("Choose someone to chat with", [u.username for u in matches])
            partner_user = next(u for u in matches if u.username == partner)
            chat_id = f"{min(st.session_state.user.id, partner_user.id)}-{max(st.session_state.user.id, partner_user.id)}"

            messages = crud.get_messages(db, chat_id)
            for m in messages:
                if m.sender_id == st.session_state.user.id:
                    st.markdown(f'<div class="chat-you">{m.content} ✅</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-partner">{m.content}</div>', unsafe_allow_html=True)

            msg = st.text_input("Type a message", key="msg_input")
            if st.button("Send"):
                if msg.strip() != "":
                    crud.create_message(db, chat_id, st.session_state.user.id, partner_user.id, msg)
                    st.experimental_rerun()
