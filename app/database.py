import motor.motor_asyncio
from beanie import init_beanie
from app.models import User, Todo

async def init_db():
    # Aapka Final Sahi URL
    MONGO_URL = "mongodb+srv://swastikaroytitu_db_user:os5IYeWZbOkUvy5I@py-todo-app.9r5dt85.mongodb.net/?retryWrites=true&w=majority"
    
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.todo_db, document_models=[User, Todo])