from fastapi import FastAPI, WebSocket
from your_script import interact_freely_with_user

app = FastAPI()

# Store active connections
active_connections = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            response = interact_freely_with_user(data)
            await websocket.send_text(response)
    except Exception as e:
        print(f"Connection with user {user_id} closed:", e)
    finally:
        del active_connections[user_id]
