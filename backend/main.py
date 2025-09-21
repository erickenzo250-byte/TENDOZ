from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connections per chat room
active_connections = {}

@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await websocket.accept()

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to everyone in the chat
            for conn in active_connections[chat_id]:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
