import asyncio
import websockets
import json

async def connect_to_ws():
    uri = "ws://127.0.0.1:8188/ws"

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket Server")

        # Example: Send a client ID (optional)
        client_id = "test_client_123"
        message = json.dumps({"clientId": client_id})
        await websocket.send(message)
        print(f"Sent: {message}")

        # Listen for incoming messages
        try:
            while True:
                response = await websocket.recv()
                print(f"Received: {response}")

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")

asyncio.run(connect_to_ws())
