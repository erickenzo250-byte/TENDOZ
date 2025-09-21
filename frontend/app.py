import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import websocket, threading

# ✅ Setup DB
Base.metadata.create_all(bind=engine)

# ------------------- WebSocket Chat ------------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ws" not in st.session_state:
    st.session_state.ws = None

def on_message(ws, message):
    st.session_state.messages.append(("Partner", message))
    st.experimental_rerun()

def connect_to_chat(chat_id):
    ws = websocket.WebSocketApp(
        "ws://localhost:8000/ws/" + chat_id,  # 🔧 update to deployed backend URL
        on_message=on_message
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
    return ws

# ------------------- Streamlit UI ------------------- #
st.set_page_config(page_title="💘 Dating Site", page_icon="💑", layout="wide")
st.title("💘 Find Your Match")

db = SessionLocal()
users = db.query(models.User).all()
db.close()

# Show profiles
cols = st.columns(2)
for i, user in enumerate(users):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div style="background:#fdf0f6;padding:20px;border-radius:12px;
                        box-shadow:2px 2px 8px rgba(0,0,0,0.1);margin-bottom:15px;">
                <h3>{user.name}, {user.age}</h3>
                <p><b>Gender:</b> {user.gender}</p>
                <p><b>Interests:</b> {user.interests}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"❤️ Chat with {user.name}", key=f"chat_{user.id}"):
            chat_id = f"match_{user.id}"  # one chat per user for demo
            st.session_state.ws = connect_to_chat(chat_id)
            st.session_state.messages = []
            st.session_state.chat_id = chat_id
            st.experimental_rerun()

# Chat box (if active)
if "chat_id" in st.session_state:
    st.subheader(f"💬 Chat Room: {st.session_state.chat_id}")

    for sender, msg in st.session_state.messages:
        st.write(f"**{sender}:** {msg}")

    msg = st.text_input("Type a message:")
    if st.button("Send") and msg and st.session_state.ws:
        st.session_state.messages.append(("Me", msg))
        st.session_state.ws.send(msg)
        st.experimental_rerun()
