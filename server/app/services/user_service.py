from app.schemas.schema import UserInfo
from fastapi import HTTPException, status

import httpx
from app.storage.crud.users import read_user, create_user

async def fetch_user_info(username : str, token: str) -> UserInfo:
    account_info = await read_user(username)
    if account_info is not None:
        return account_info
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}"
        
        # Получение данных о пользователе
        user_response = await client.get(url, headers=headers)
        if user_response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Пользователь не найден"
            )
        elif user_response.status_code == 403:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Доступ к информации о пользователе ограничен"
            )
        elif user_response.status_code != 200:
            print(user_response)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Ошибка при получении данных пользователя"
            )
        user_data = user_response.json()
        
        # Получение списка репозиториев пользователя
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_response = await client.get(repos_url, headers=headers)
        repos_data = repos_response.json()
        
        # Получение списка гистов пользователя
        gists_url = f"https://api.github.com/users/{username}/gists"
        gists_response = await client.get(gists_url, headers=headers)
        gists_data = gists_response.json()

        team_counter = 0
        repos = []
        for repo in repos_data:
            repos.append(repo.get('full_name', {}))
            cnt = await get_collaborators_count(client, repo.get("owner", {}).get("login"), repo.get("name", {}), token)
            if int(cnt) > 1:
                team_counter += 1
        
        # Формируем результат
        account_info = UserInfo(
            username=username,
            name=user_data.get("name"),
            email=user_data.get("email"),
            team_projects=team_counter,
            solo_projects=(len(repos_data) - team_counter),
            solo_gist=len(gists_data),
            account_age=(2024 - int(user_data.get("created_at", "")[:4])),
            avatar_url=user_data.get("avatar_url"),
            html_url=user_data.get("html_url"),
            followers=user_data.get("followers"),
            following=user_data.get("following"),
            repos=repos
        )

        account_info = await create_user(account_info)
        
    return account_info

async def get_collaborators_count(client, owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        collaborators = response.json()
        return len(collaborators)  # Количество коллабораторов
    elif response.status_code == 404:
        return "Репозиторий не найден"
    elif response.status_code == 403:
        print("Доступ к репозиторию ограничен", owner, repo)
        return 1
    else:
        return f"Ошибка: {response.status_code} - {response.reason}"