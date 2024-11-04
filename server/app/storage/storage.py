from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from app.config.config import get_mongo
import zipfile
import json
from pymongo import MongoClient
from typing import Dict, Any
import os

# Подключение к MongoDB
MONGO_DETAILS = get_mongo()
client = AsyncIOMotorClient(MONGO_DETAILS)

# Создание баз данных и коллекций
db = client["git_cache"]
user_collection = db["users"]
repo_stat_collection = db["repo_stats"]
account_collection = db["accounts"]
summary_collection = db["summaries"]

user_comp_collection = db['user_comp']

async def extract_and_save_users(zip_path="hardskills_with_repo.zip"):
    """
    Извлекает JSON файлы из zip архива, добавляет в каждый объект поле username (имя файла без расширения),
    и сохраняет его в коллекцию MongoDB.
    
    Args:
        zip_path (str): Путь к zip архиву.
    """
    with zipfile.ZipFile(zip_path, 'r') as archive:
        print("Archive")
        for file_name in archive.namelist():
            print("Archive")
            if file_name.endswith('.json'):
                with archive.open(file_name) as json_file:
                    # Загрузка данных из JSON файла
                    data = json.load(json_file)
                    
                    # Извлечение имени файла без расширения и добавление его как username
                    username = os.path.splitext(os.path.basename(file_name))[0]
                    data['username'] = username
                    
                    # Сохранение объекта в коллекцию MongoDB
                    user_comp_collection.insert_one(data)

async def get_all_users():
    all_users = await user_comp_collection.distinct('username')
    return all_users

async def get_objects_by_username(username):
    """
    Получает все объекты из коллекции user_comp по имени пользователя.
    
    Args:
        username (str): Имя пользователя.
        
    Returns:
        list: Список объектов (словарей) пользователя из коллекции.
    """
    all_users = await user_comp_collection.find().to_list(None)  # None для получения всех документов
    print(all_users)
    user_objects = await user_comp_collection.find({'username': username}).to_list(None)  # Use to_list with await
    # print(fff, username, "############################", user_objects)
    
    return user_objects

async def get_usernames_by_competency(competency):
    """
    Получает список уникальных имен пользователей, у которых есть заданная компетенция.
    
    Args:
        competency (str): Название компетенции для поиска (например, 'frontend').
        
    Returns:
        list: Список уникальных имен пользователей с указанной компетенцией.
    """
    
    usernames = await user_comp_collection.distinct('username', {f'competencies.{competency}': {'$exists': True}})
    return usernames

async def is_collection_empty():
    """
    Проверяет, пуста ли указанная коллекция.
    
    Args:
        collection: Коллекция MongoDB.
        
    Returns:
        bool: True, если коллекция пуста, иначе False.
    """
    count = user_comp_collection.count_documents({})
    return count == 0


