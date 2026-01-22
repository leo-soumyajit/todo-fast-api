import motor.motor_asyncio
from beanie import init_beanie
from app.models import User, Todo

async def init_db():
    # Bhai, apni MongoDB connection string yahan replace karna
    # Password me special characters ho to URL encode karna mat bhulna
    MONGO_URL = "mongodb+srv://swastikaroytitu_db_user:os5IYeWZbOkUvy5I@cluster0.mongodb.net/?retryWrites=true&w=majority"
    
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    
    # Database ka naam 'todo_db' rakha hai
    await init_beanie(database=client.todo_db, document_models=[User, Todo])