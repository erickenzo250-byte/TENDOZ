import streamlit as st
import requests
import asyncio
import websockets

BASE_URL = "http://localhost:8000"  # Change to deployed backend

st.sidebar.title("Dating App")
menu = ["My Profile", "Explore", "Chat"]
choice = st.sidebar.radio("Menu", menu)

if "user_id" not in st.session_state:
    st.session_state.user_id = 1  # mock login

# ---------- PROFILE ----------
if choice == "My Profile":
    st.header("👤 My Profile")
    res = requests.get(f"{BASE_URL}/users/{st.session_state.user_id}")
    if res.ok:
        user = res.json()
        st.write(f"**{user['username']}** ({user['age']}, {user['gender']})")
        st.write(f"✨ Interests: {user['interests']}")
        st.write(f"💬 Bio: {user['bio']}")
    else:
        st.error("User not found")

# ---------- EXPLORE ----------
elif choice == "Explore":
    st.header("🌍 Explore Profiles")
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    min_age, max_age = st.slider("Age Range", 18, 100, (20, 40))
    interest = st.text_input("Interest")

    params = {"min_age": min_age, "max_age": max_age}
    if gender:
        params["gender"] = gender
    if interest:
        params["interest"] = interest

    res = requests.get(f"{BASE_URL}/explore", params=params)
    if res.ok:
        for u in res.json():
            if u["id"] == st.session_state.user_id: continue
            st.subheader(f"{u['username']} ({u['age']}, {u['gender']})")
            st.write(u["bio"])
            st.write(f"✨ {u['interests']}")
            if st.button(f"Like {u['username']}", key=u["id"]):
                r = requests.post(f"{BASE_URL}/like/", params={"liker_id": st.session_state.user_id, "liked_id": u["id"]})
                result = r.json()
                if result["match"]:
                    st.success("💖 It's a match! Start chatting.")

# ---------- CHAT ----------
elif choice == "Chat":
    st.header("💬 Chat")
    receiver_id = st.number_input("Chat with user ID", min_value=1, step=1)
    msg = st.text_input("Message")
    if st.button("Send"):
        async def send_message():
            async with websockets.connect(f"ws://localhost:8000/ws/{st.session_state.user_id}") as ws:
                await ws.send(f"{receiver_id}|{msg}")
        asyncio.run(send_message())
    st.info("Real-time chat coming here (typing, emojis, receipts)")
