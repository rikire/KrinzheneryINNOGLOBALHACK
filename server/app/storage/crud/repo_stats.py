from app.schemas.schema import UserRepoStat
from bson.objectid import ObjectId
from ..storage import repo_stat_collection
from typing import List
from fastapi import HTTPException, status

async def repo_stat_exists(username: str, repo_name: str) -> bool:
    return bool(
        await repo_stat_collection.find_one({"username": username, "repo_name": repo_name})
    )

# Создать пользователя
async def create_repo_stat(repo_stat_data: UserRepoStat) -> UserRepoStat:
    if await repo_stat_exists(repo_stat_data.username, repo_stat_data.repo_name):
        return await update_repo_stat(repo_stat_data)
    else:
        result = await repo_stat_collection.insert_one(repo_stat_data.model_dump())
        if result.inserted_id:
            return repo_stat_data
        return None

# Прочитать пользователя
async def read_repo_stat(username: str, repo_name: str) -> UserRepoStat:
    repo_stat = await repo_stat_collection.find_one({"username": username, "repo_name": repo_name})
    return UserRepoStat(**repo_stat) if repo_stat else None

# Прочитать пользователя
async def read_repo_stat_by_username(username: str) -> List[UserRepoStat]:
    cursor = repo_stat_collection.find({"username": username})
    repo_stats = await cursor.to_list(length=None)
    return [UserRepoStat(**repo_stat) for repo_stat in repo_stats]

# Прочитать пользователя
async def read_repo_stat_by_repo_name(repo_name: str) -> List[UserRepoStat]:
    repo_stats = await repo_stat_collection.find({"repo_name": repo_name})
    return [UserRepoStat(**repo_stat) for repo_stat in repo_stats]


# Обновить пользователя
async def update_repo_stat(repo_stat_data: UserRepoStat) -> UserRepoStat:
    update_result = await repo_stat_collection.update_one(
        {
            "username": repo_stat_data.username,
            "repo_name": repo_stat_data.repo_name
        },
        {"$set": repo_stat_data.model_dump()}
    )

    if update_result.modified_count:
        return repo_stat_data

    return None

# Удалить пользователя
async def delete_repo_stat(username: str, repo_name: str):
    res = await repo_stat_collection.delete_one({"username": username, "repo_name": repo_name})
    if res.deleted_count:
        return status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

