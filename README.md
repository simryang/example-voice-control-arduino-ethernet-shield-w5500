# 🎤 Voice-Controlled Arduino with WIZnet Ethernet Shield

This project demonstrates how to control an Arduino board using **voice commands** through a **web browser**. Voice input is processed using the **Web Speech API**, and the command is sent to a **FastAPI server**, which the Arduino fetches and executes via Ethernet.

> Based on and inspired by the original tutorial:  
> 👉 https://www.instructables.com/Voice-Control-Arduino-Ethernet-Shield-module-Wizne/

---

## 🔧 Components

- Arduino Uno or Mega
- WIZnet W5100 or W5500 Ethernet Shield
- LED (connected to digital pin)
- LAN Cable (connected to your local network)
- PC running FastAPI server

---

## 📂 Files

- `client.ino` – Arduino sketch to fetch and execute commands.
- `server.py` – FastAPI server with embedded HTML voice recognition interface.
- `README.md` – This guide.

---

## ⚙️ How It Works

1. User opens a browser and speaks: **"Turn on"** or **"Turn off"**.
2. The voice is converted to text using Web Speech API.
3. A POST request is sent to `server.py` with the command.
4. Arduino periodically performs a GET request to fetch the latest command.
5. Based on the command, it turns the LED ON or OFF.

---

## 🚀 Running the FastAPI Server

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run the server

```python
python server.py
```

The server will:

- Start on `http://localhost:8000`
- Serve an HTML page for voice input at `/`
- Accept `POST`/`GET` to `/command` for the client

---

## 🖥️ Using the Voice Interface

1. Open [`http://localhost:8000`](http://localhost:8000) in **Google Chrome**.
2. Allow microphone access.
3. Click **"🎙 Click to Speak"** and say:
   - `Turn on`
   - `Turn off`
4. The command is sent to the server.

> ⚠️ **Note:** Works only on browsers that support `webkitSpeechRecognition`  
> (e.g., **Chrome desktop**, **Samsung mobile browser**)

---

## 🔌 Uploading the Arduino Sketch

1. Open `client.ino` in **Arduino IDE**.
2. Configure the following:
   - **MAC address**
   - **Static IP** (if needed)
   - **Your FastAPI server IP** (`serverName`)
   - **Ethernet shield model** (W5100/W5500)
3. Upload and connect the board to the **same LAN** as your PC.
