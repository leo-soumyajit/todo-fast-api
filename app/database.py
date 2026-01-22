# app/database.py

async def init_db():
    # Make sure 'cluster0' ke baad wo random code (e.g., .rx89q) zaroor ho!
    MONGO_URL = "mongodb+srv://swastikaroytitu_db_user:os5IYeWZbOkUvy5I@cluster0.<YOUR_UNIQUE_CODE>.mongodb.net/?retryWrites=true&w=majority"
    
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.todo_db, document_models=[User, Todo])