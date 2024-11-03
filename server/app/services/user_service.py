from app.schemas.schema import UserInfo
from fastapi import HTTPException, status

import httpx
from app.storage.crud.users import read_user, create_user
from datetime import datetime
from fastapi import HTTPException, status
import httpx

import requests
import os

async def fetch_user_info(username: str, token: str) -> UserInfo:
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
        # Parse the creation date and calculate account age in months
        created_at_str = user_data.get("created_at", "")
        created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
        current_date = datetime.utcnow()
        account_age_months = (current_date.year - created_at.year) * 12 + current_date.month - created_at.month
        
        account_info = UserInfo(
            username=username,
            name=user_data.get("name"),
            email=user_data.get("email"),
            team_projects=team_counter,
            solo_projects=(len(repos_data) - team_counter),
            solo_gist=len(gists_data),
            account_age=account_age_months,  # Store age in months
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

import requests

async def fetch_user_soft_skills(username, token):    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://api.github.com/search/issues?q=author:{username}+is:issue&per_page=10&page=0", headers=headers)
    
    if response.status_code != 200:
        return response
    
    user_issues = response.json()
    data = ""
    if user_issues:
        for issue in user_issues["items"]:
            if issue.get("body"):
                data += issue["body"]
    else:
        return {"soft_skills": ""}
    
    # Prompt to assess user comments
    url = "https://vk-devinsight-case.olymp.innopolis.university/generate"
    prompt = "Оцени комментарии пользователя и дай характеристику его навыкам вежливости, уважения, грамотности, инициативности, ответственности и других качеств, которые ты можешь определить. Приведи несколько предложений на русском языке в формате сплошного текста без использования разметки.\nКомментарии:\n"

    request_data = {
        "prompt": [prompt + data],
        "stream": False,
        "max_tokens": 500,
        "temperature": 0.5,
        "seed": 42,
    }
    headers = {"Content-Type": "application/json"}

    # Use `request_data` instead of `data` as JSON payload
    response_lama = requests.post(url, json=request_data, headers=headers)
    
    if response_lama.status_code == 200:
        # Get the JSON content from the response
        result = response_lama.json()
        return {"soft_skills": result}
    else:
        return {"error": f"Failed to fetch soft skills, status code: {response_lama.status_code}"}

    
