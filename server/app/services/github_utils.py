import asyncio
import httpx
from typing import List, Dict
import datetime

async def fetch_issues(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    print(url)
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Возвращает список issues
    else:
        print(f"Ошибка получения issues: Статус {response.status_code} - {response.text}")
        return None

def user_has_issues(issues, username):
    """Проверяет, есть ли у пользователя issues."""
    if issues is None:
        return False
    # Фильтруем issues по пользователю
    return any(issue.get('user', {}).get('login') == username for issue in issues)

async def check_user_issues(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        issues = await fetch_issues(client, owner, repo, token)
        return user_has_issues(issues, username)
    


async def fetch_pull_requests(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Возвращает список pull requests
    else:
        print(f"Ошибка получения pull requests: Статус {response.status_code} - {response.text}")
        return None

def user_has_pull_requests(pull_requests, username):
    """Проверяет, есть ли у пользователя pull requests."""
    if pull_requests is None:
        return False
    # Фильтруем pull requests по пользователю
    return any(pr.get('user', {}).get('login') == username for pr in pull_requests)

async def check_user_pull_requests(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        pull_requests = await fetch_pull_requests(client, owner, repo, token)
        return user_has_pull_requests(pull_requests, username)
    


async def fetch_commits_by_author(client: httpx.AsyncClient, owner: str, repo: str, token: str, username: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?author={username}"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Возвращает список коммитов
    else:
        print(f"Ошибка получения коммитов: Статус {response.status_code} - {response.text}")
        return None

async def check_user_commits(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        commits = await fetch_commits_by_author(client, owner, repo, token, username)
        return commits is not None and len(commits) > 0
    


async def fetch_projects(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/projects"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Возвращает список проектов
    else:
        print(f"Ошибка получения проектов: Статус {response.status_code} - {response.text}")
        return None

def user_has_projects(projects, username):
    """Проверяет, есть ли у пользователя проекты."""
    if projects is None:
        return False
    # Фильтруем проекты по пользователю
    return any(project.get('creator', {}).get('login') == username for project in projects)

async def check_user_projects(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        projects = await fetch_projects(client, owner, repo, token)
        return user_has_projects(projects, username)
    


async def fetch_workflow_runs(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('workflow_runs', [])  # Возвращает список запусков (workflow runs)
    else:
        print(f"Ошибка получения запусков: Статус {response.status_code} - {response.text}")
        return None

def user_has_actions(runs, username):
    """Проверяет, есть ли у пользователя действия (Actions)."""
    if runs is None:
        return False
    # Фильтруем запуски по пользователю
    return any(run.get('actor', {}).get('login') == username for run in runs)

async def check_user_actions(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        runs = await fetch_workflow_runs(client, owner, repo, token)
        return user_has_actions(runs, username)


async def fetch_releases(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список релизов
    else:
        print(f"Ошибка получения релизов: Статус {response.status_code} - {response.text}")
        return None

def user_has_releases(releases, username):
    """Проверяет, есть ли у пользователя релизы."""
    if releases is None:
        return False
    # Фильтруем релизы по пользователю
    return any(release.get('author', {}).get('login') == username for release in releases)

async def check_user_releases(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        releases = await fetch_releases(client, owner, repo, token)
        return user_has_releases(releases, username)


async def fetch_issues(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список issues
    else:
        print(f"Ошибка получения issues: Статус {response.status_code} - {response.text}")
        return None

async def fetch_issue_comments(client: httpx.AsyncClient, owner: str, repo: str, issue_number: int, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список комментариев к issue
    else:
        print(f"Ошибка получения комментариев к issue {issue_number}: Статус {response.status_code} - {response.text}")
        return None

async def check_user_issue_comments(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        issues = await fetch_issues(client, owner, repo, token)

        if issues is None:
            return False

        # Проверяем комментарии ко всем issues
        for issue in issues:
            comments = await fetch_issue_comments(client, owner, repo, issue['number'], token)
            if comments is not None:
                # Проверяем, есть ли комментарии от указанного пользователя
                if any(comment.get('user', {}).get('login') == username for comment in comments):
                    return True  # Найден комментарий пользователя

    return False  # Комментариев от пользователя не найдено


async def fetch_pull_requests(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список pull request
    else:
        print(f"Ошибка получения pull requests: Статус {response.status_code} - {response.text}")
        return None

async def fetch_pull_request_comments(client: httpx.AsyncClient, owner: str, repo: str, pull_number: int, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список комментариев к pull request
    else:
        print(f"Ошибка получения комментариев к pull request {pull_number}: Статус {response.status_code} - {response.text}")
        return None

async def check_user_pull_request_comments(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        pull_requests = await fetch_pull_requests(client, owner, repo, token)

        if pull_requests is None:
            return False

        # Проверяем комментарии ко всем pull request
        for pull_request in pull_requests:
            comments = await fetch_pull_request_comments(client, owner, repo, pull_request['number'], token)
            if comments is not None:
                # Проверяем, есть ли комментарии от указанного пользователя
                if any(comment.get('user', {}).get('login') == username for comment in comments):
                    return True  # Найден комментарий пользователя

    return False  # Комментариев от пользователя не найдено


async def fetch_commits(client: httpx.AsyncClient, owner: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список коммитов
    else:
        print(f"Ошибка получения коммитов: Статус {response.status_code} - {response.text}")
        return None

async def fetch_commit_comments(client: httpx.AsyncClient, owner: str, repo: str, commit_sha: str, token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/comments"
    headers = {"Authorization": f"token {token}"}
    response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает список комментариев к коммиту
    else:
        print(f"Ошибка получения комментариев к коммиту {commit_sha}: Статус {response.status_code} - {response.text}")
        return None

async def check_user_commit_comments(owner: str, repo: str, username: str, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        commits = await fetch_commits(client, owner, repo, token)

        if commits is None:
            return False

        # Проверяем комментарии ко всем коммитам
        for commit in commits:
            comments = await fetch_commit_comments(client, owner, repo, commit['sha'], token)
            if comments is not None:
                # Проверяем, есть ли комментарии от указанного пользователя
                if any(comment.get('user', {}).get('login') == username for comment in comments):
                    return True  # Найден комментарий пользователя

    return False  # Комментариев от пользователя не найдено