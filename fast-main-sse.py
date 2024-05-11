from fastapi import FastAPI, Response
from your_script import interact_freely_with_user
import asyncio

app = FastAPI()

async def generate_responses():
    for i in range(10):
        user_input = yield f"Message {i}"
        response = interact_freely_with_user(user_input)
        yield response
        await asyncio.sleep(1)

async def send_events(response: Response):
    async for event in generate_responses():
        response.body.write(event.encode())
        response.body.write(b"\n\n")
        await response.is_disconnected()

@app.get("/stream")
async def stream(response: Response):
    response.headers['Content-Type'] = 'text/event-stream'
    await send_events(response)
    return response

@app.post("/send-message")
async def send_message(user_input: str):
    # Process the user's input and generate a response
    response = interact_freely_with_user(user_input)
    return {"response": response}

@app.get("/")
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSE Example</title>
        <script>
            const eventSource = new EventSource('/stream');
            eventSource.onmessage = function(event) {
                console.log(event.data);
                // Handle incoming events
            };
        </script>
    </head>
    <body>
        <h1>SSE Example</h1>
    </body>
    </html>
    """
