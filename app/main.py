import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from app.routes.chat import router as chat_router

load_dotenv()

app = FastAPI(
    title="Claude Chat API",
    description="A FastAPI application for chatting with Claude",
    version="1.0.0"
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    """Serve the chat UI."""
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return FileResponse(os.path.join(static_path, "chat.html"))


# Include routers
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
