from app.schemas.schema import SearchResult
from app.storage.crud.users import read_all_users
from app.services.repo_service import fetch_global_stat

async def fetch_search(querry:str, token: str) -> SearchResult:
    parts = querry.split()
    users = await read_all_users()
    users_marks = []
    for user in users:
        mark = 0
        stat = await fetch_global_stat(user.username, token)
        for part in parts:
            if part in stat.competencies:
                mark -= 1000
            if part in user.languages:
                mark -= 100
            if part in user.stack:
                mark -= 10
        if mark < 0:
            users_marks.append((mark, user))
    
    sorted_data = [v for (k, v) in sorted(users_marks)]
    return SearchResult(developers=sorted_data)
    