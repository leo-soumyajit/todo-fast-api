from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, todos
from contextlib import asynccontextmanager

# Database Lifecycle Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() # Startup pe DB connect karo
    yield
    # Shutdown logic agar chahiye to yahan aayega

app = FastAPI(lifespan=lifespan, title="Todo App Backend")

# CORS Setup (Frontend React ke liye zaroori hai)
# "*" ka matlab koi bhi frontend connect kar sakta hai (Development ke liye ok hai)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes Jodo
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Todo Backend is Running! 🚀"}