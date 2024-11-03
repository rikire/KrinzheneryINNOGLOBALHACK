from typing import List, Optional
from ..storage import account_collection
from bson import ObjectId

from app.models.models import Account

# CRUD функции

def create_account(account_data: Account) -> str:
    """Создание аккаунта"""
    account_dict = account_data.dict()
    result = account_collection.insert_one(account_dict)
    return str(result.inserted_id)

def get_account(login: str) -> Optional[Account]:
    """Получение аккаунта по ID"""
    account_data = account_collection.find_one({"login": login})
    return Account(**account_data) if account_data else None

def update_account(login: str, account_data: Account) -> bool:
    """Обновление аккаунта по ID"""
    result = account_collection.update_one(
        {"login": login},
        {"$set": account_data.dict()}
    )
    return result.modified_count > 0

def delete_account(login: str) -> bool:
    """Удаление аккаунта по ID"""
    result = account_collection.delete_one({"login": login})
    return result.deleted_count > 0

def list_accounts() -> List[Account]:
    """Получение списка всех аккаунтов"""
    accounts = account_collection.find()
    return [Account(**account) for account in accounts]

