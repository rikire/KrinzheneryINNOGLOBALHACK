from app.models.models import RepoStat
from bson.objectid import ObjectId
from ..storage import user_collection
from typing import List

# Создать пользователя
async def create_repo_stat(repo_stat_data: RepoStat) -> RepoStat:
    pass

# Прочитать пользователя
async def read_repo_stat(username: str, repo_name: str) -> RepoStat:
    pass

# Прочитать пользователя
async def read_repo_stat_by_username(username: str) -> List[RepoStat]:
    pass

# Прочитать пользователя
async def read_repo_stat_by_repo_name(repo_name: str) -> List[str]:
    pass


# Обновить пользователя
async def update_repo_stat(user_data: RepoStat) -> RepoStat:
    pass

# Удалить пользователя
async def delete_repo_stat(username: str) -> RepoStat:
    pass


