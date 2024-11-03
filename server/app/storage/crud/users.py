from app.schemas.schema import UserInfo
from bson.objectid import ObjectId
from ..storage import user_collection
from typing import List, Optional

async def user_exists(username: str) -> bool:
    user_data = await user_collection.find_one({"username": username})
    return user_data is not None

async def create_user(user_data: UserInfo) -> UserInfo:
    await user_collection.insert_one(user_data.dict())
    return user_data

# Прочитать всех пользователей
async def read_all_users() -> List[UserInfo]:
    users = []
    async for user in user_collection.find():
        users.append(UserInfo(**user))
    return users

# Прочитать пользователя по username
async def read_user(username: str) -> Optional[UserInfo]:
    user_data = await user_collection.find_one({"username": username})
    if user_data:
        return UserInfo(**user_data)
    return None

# Обновить пользователя
async def update_user(user_data: UserInfo) -> Optional[UserInfo]:
    result = await user_collection.update_one({"username": user_data.username}, {"$set": user_data.dict()})
    if result.modified_count:
        return user_data
    return None

# Удалить пользователя
async def delete_user(username: str) -> Optional[UserInfo]:
    user_data = await user_collection.find_one_and_delete({"username": username})
    if user_data:
        return UserInfo(**user_data)
    return None

