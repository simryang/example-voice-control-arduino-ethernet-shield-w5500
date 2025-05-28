from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# 명령 저장용 전역 변수
latest_command = "None"

class Command(BaseModel):
    command: str

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 명령어 조회
@app.get("/command", response_class=PlainTextResponse)
async def get_command():
    return latest_command

# 명령어 저장
@app.post("/command")
async def post_command(cmd: Command):
    global latest_command
    latest_command = cmd.command
    return {"message": f"Command '{cmd.command}' received."}

# HTML 페이지 직접 반환
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Voice Control</title>
    </head>
    <body>
        <h1>🎤 Voice Control for Arduino</h1>
        <p><strong>Say:</strong> "Turn on" or "Turn off"</p>
        <button onclick="startListening()">🎙 Click to Speak</button>
        <p id="status">Waiting for voice input...</p>

        <script>
            function startListening() {
                const status = document.getElementById("status");

                if (!('webkitSpeechRecognition' in window)) {
                    status.innerText = "Speech recognition not supported in this browser.";
                    return;
                }

                const recognition = new webkitSpeechRecognition();
                recognition.lang = "en-US";
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.start();

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript.trim();
                    status.innerText = `Heard: ${transcript}`;

                    if (transcript === "Turn on" || transcript === "Turn off") {
                        fetch("/command", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ command: transcript })
                        })
                        .then(response => response.json())
                        .then(data => {
                            status.innerText += ` → Sent to server: ${data.message}`;
                        })
                        .catch(error => {
                            status.innerText = `Error sending command: ${error}`;
                        });
                    } else {
                        status.innerText += " → Invalid command.";
                    }
                };

                recognition.onerror = function(event) {
                    status.innerText = `Speech error: ${event.error}`;
                };
            }
        </script>
    </body>
    </html>
    """
    return html_content

# main 구문에서 자동 실행
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
