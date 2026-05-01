# Claude Chat - FastAPI Application

A FastAPI web application that provides a chat interface for communicating with Claude (Anthropic API).

## Features

- Web-based chat interface with streaming responses
- Conversation history support
- Real-time response streaming using Server-Sent Events (SSE)
- Clean, modern UI with dark theme

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy the example environment file and add your Anthropic API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Get your API key from: https://console.anthropic.com/

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

### 4. Open in Browser

Navigate to: http://localhost:8000

## API Endpoints

### POST /api/chat
Send a message and get a response.

```json
{
    "message": "Hello, Claude!",
    "conversation_history": [],
    "system_prompt": "You are a helpful assistant.",
    "max_tokens": 1024
}
```

### POST /api/chat/stream
Stream a response using Server-Sent Events (SSE).

Same request body as `/api/chat`, but returns a streaming response.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py          # Chat endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── claude.py        # Claude API client
│   └── static/
│       └── chat.html        # Web UI
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
└── README.md
```

## Usage

1. Open the application in your browser
2. Type your message in the input field
3. Press Enter or click Send
4. Claude's response will stream in real-time
5. Use "Clear" to reset the conversation
