from app.models.models import UserInfo
from bson.objectid import ObjectId
from ..storage import user_collection
from typing import List

# Создать пользователя
async def create_user(user_data: UserInfo) -> UserInfo:
    pass

async def read_all_users() -> List[UserInfo]:
    pass

# Прочитать пользователя
async def read_user(username: str) -> UserInfo:
    pass

# Обновить пользователя
async def update_user(user_data: UserInfo) -> UserInfo:
    pass

# Удалить пользователя
async def delete_user(username: str) -> UserInfo:
    pass


