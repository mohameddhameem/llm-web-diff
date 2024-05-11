from flask import Flask, render_template, Response
from src.teach import interact_with_script

app = FastAPI()

@app.post("/chat")
async def chat(user_input: str = Form(...)):
    response = interact_with_script(user_input)
    return {"response": response}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def generate_responses():
    for response in interact_freely_with_user():
        yield f"data: {response}\n\n"

@app.route('/stream')
def stream():
    return Response(generate_responses(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)