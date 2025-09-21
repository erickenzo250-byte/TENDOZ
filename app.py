import streamlit as st
from backend.database import SessionLocal, engine, Base
from backend import crud, models

# Create DB tables
Base.metadata.create_all(bind=engine)
db = SessionLocal()

st.set_page_config(page_title="💖 Dating App", layout="wide")

# --- Session State ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- Sidebar Menu ---
menu = ["My Profile", "Explore", "Chat"]
choice = st.sidebar.radio("Menu", menu)

# --- MY PROFILE ---
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

# --- EXPLORE ---
elif choice == "Explore":
    st.title("🌍 Explore Profiles")

    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        # Filters
        st.sidebar.subheader("Filters")
        gender_filter = st.sidebar.selectbox("Gender", ["Any", "Male", "Female", "Other"])
        age_range = st.sidebar.slider("Age Range", 18, 100, (20, 40))
        interest_filter = st.sidebar.text_input("Interest Contains", "")

        # Get users
        users = crud.get_users(db, exclude_id=st.session_state.user.id)
        filtered = []
        for u in users:
            if gender_filter != "Any" and u.gender != gender_filter:
                continue
            if not (age_range[0] <= u.age <= age_range[1]):
                continue
            if interest_filter and interest_filter.lower() not in u.interests.lower():
                continue
            filtered.append(u)

        if not filtered:
            st.info("No profiles found.")
        else:
            for u in filtered:
                with st.container():
                    st.subheader(f"{u.username} ({u.age}, {u.gender})")
                    st.write(f"💬 {u.bio}")
                    st.write(f"✨ Interests: {u.interests}")
                    if st.button(f"Like {u.username}", key=f"like_{u.id}"):
                        # Here you could implement match logic later
                        st.success(f"You liked {u.username}!")

                    st.markdown("---")

# --- CHAT ---
elif choice == "Chat":
    st.title("💬 Chat")

    if not st.session_state.user:
        st.warning("Please log in first (My Profile).")
    else:
        users = crud.get_users(db, exclude_id=st.session_state.user.id)
        if not users:
            st.info("No users to chat with yet.")
        else:
            partner = st.selectbox("Choose someone to chat with", [u.username for u in users])
            partner_user = next(u for u in users if u.username == partner)
            chat_id = f"{min(st.session_state.user.id, partner_user.id)}-{max(st.session_state.user.id, partner_user.id)}"

            # Display past messages
            messages = crud.get_messages(db, chat_id)
            for m in messages:
                sender = "You" if m.sender_id == st.session_state.user.id else partner_user.username
                st.write(f"**{sender}**: {m.content} ({m.timestamp})")

            # Send new message
            msg = st.text_input("Type a message", key="msg_input")
            if st.button("Send"):
                if msg.strip() != "":
                    crud.create_message(db, chat_id, st.session_state.user.id, partner_user.id, msg)
                    st.experimental_rerun()
