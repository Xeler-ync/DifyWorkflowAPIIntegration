import asyncio
import websockets
import json
from config import config
from sentiment_analysis import get_sentiment


async def websocket_client():
    uri = f"ws://localhost:{config.port}/api/sentiment_analysis"
    retry_delay = 2  # seconds
    retry_count = 0

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to the server")
                retry_count = 0

                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)

                        response_data = {
                            "id": data["id"],
                            "status": "success",
                            "data": get_sentiment(data["content"])["sentiment_score"],
                        }
                        # response_data["data"] is float, from -1 to 1. 0 is neutral, >0 is positive, <0 is negative

                        response_message = json.dumps(response_data)
                        await websocket.send(response_message)
                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed: {e.reason}")
                        break

        except Exception as e:
            retry_count += 1
            print(
                f"Connection failed: {e}, retrying in {retry_delay} seconds... (retry count: {retry_count})"
            )
            await asyncio.sleep(retry_delay)


asyncio.run(websocket_client())
