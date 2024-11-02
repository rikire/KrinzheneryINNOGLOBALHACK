from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

# Подключение к MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)

# Создание баз данных и коллекций
db = client["git_cache"]
user_collection = db["users"]
repo_stat_collection = db["repo_stats"]
account_collection = db["accounts"]
summary_collection = db["summaries"]