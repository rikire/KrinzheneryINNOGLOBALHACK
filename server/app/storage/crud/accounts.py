from typing import List, Optional
from ..storage import account_collection
from bson import ObjectId

from app.models.models import Account

# CRUD функции

async def create_account(account_data: Account) -> str:
    """Создание аккаунта"""
    account_dict = account_data.dict()
    result = await account_collection.insert_one(account_dict)
    return str(result.inserted_id)

async def get_account(login: str) -> Optional[Account]:
    """Получение аккаунта по ID"""
    account_data = await account_collection.find_one({"login": login})
    return Account(**account_data) if account_data else None

async def update_account(login: str, account_data: Account) -> bool:
    """Обновление аккаунта по ID"""
    result = await account_collection.update_one(
        {"login": login},
        {"$set": account_data.dict()}
    )
    return result.modified_count > 0

async def delete_account(login: str) -> bool:
    """Удаление аккаунта по ID"""
    result = await account_collection.delete_one({"login": login})
    return result.deleted_count > 0

async def list_accounts() -> List[Account]:
    """Получение списка всех аккаунтов"""
    accounts = await account_collection.find()
    return [Account(**account) for account in accounts]
