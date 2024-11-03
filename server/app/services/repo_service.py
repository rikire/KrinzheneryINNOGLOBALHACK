from app.storage.crud.repo_stats import read_repo_stat_by_username, read_repo_stat, repo_stat_exists, create_repo_stat
from app.schemas.schema import UserGlobalStat, ActivityList, UserRepoStat, UserCompetencyProfile
from app.services.github_utils import check_user_actions, check_user_projects, check_user_commit_comments, check_user_commits, check_user_issues, check_user_issue_comments, check_user_pull_request_comments, check_user_pull_requests, check_user_releases
from app.services.user_service import fetch_user_info
from app.external.get_metrics_from_local import get_hardskills_from_llama
import git
import asyncio
import httpx
from typing import List, Dict, Tuple
import datetime
import os
from fastapi import HTTPException
from collections import defaultdict

async def fetch_repo_stat(username: str, owner: str, repo: str, token: str, target: str) -> UserRepoStat:
    """
    Получение статистики репозитория из кэша или GitHub API.

    Args:
        username (str): Имя пользователя на GitHub.
        owner (str): Владелец репозитория.
        repo (str): Название репозитория.
        token (str): Токен доступа к GitHub API.

    Returns:
        RepoStat: Статистика репозитория.
    """
    repo_full_name = f"{owner}/{repo}"
    if await repo_stat_exists(username, repo_full_name):
        return await read_repo_stat(username, repo_full_name)

    if target == "local":
        repo_stat = await get_local_repo_stat(username, owner, repo, token)
    elif target == "github":
        repo_stat = await get_github_repo_stat(username, owner, repo, token)
    else:
        raise ValueError(f"Invalid target: {target}")

    await create_repo_stat(repo_stat)
    return repo_stat

async def get_local_repo_stat(username: str, owner: str, repo: str, token: str) -> UserRepoStat:
    """
    Получение статистики репозитория из локального Git репозитория.

    Args:
        username (str): Имя пользователя на GitHub.
        owner (str): Владелец репозитория.
        repo (str): Название репозитория.
        token (str): Токен доступа к GitHub API (здесь не используется).

    Returns:
        UserRepoStat: Статистика репозитория.
    """

    local_repo = None
    repo_path = f"./dataset/{repo}"
   
    os.makedirs("dataset", exist_ok=True)
   
    try:
        local_repo = git.Repo(repo_path)
    except git.exc.NoSuchPathError:
        gitclone = git.Repo.clone_from(f"https://github.com/{owner}/{repo}.git", repo_path)
        if gitclone is None:
            raise Exception(f"Не удалось клонировать репозиторий {owner}/{repo}.")
        local_repo = git.Repo(repo_path)
    
    # Получение коммитов автора
    # name, mail, username
    user_info = await fetch_user_info(username=username, token=token)
    name = user_info.name
    mail = user_info.email
    
    author_name = username
    
    # Пробуем различные критерии поиска автора
    author_commits = list(local_repo.iter_commits(author=author_name))
    if not author_commits:
        author_name = name
        author_commits = list(local_repo.iter_commits(author=author_name))
    if not author_commits:
        author_name = mail
        author_commits = list(local_repo.iter_commits(author=author_name))
    if not author_commits:
        raise HTTPException(status_code=404, detail="Автор коммитов не найден")
    
    repo_stat = UserRepoStat(
        username=username,
        repo_name=f"{owner}/{repo}",
        repo_html_url=f"https://github.com/{owner}/{repo}",
        using_github_features=[],
        commits_total=0,
        commits_per_day=0,  
        commits_per_week=0,
        commits_per_year=0,
        average_commit_size=0,
        competencies = None
    )
    print(author_name)
    # Вычисление статистики коммитов
    repo_stat.commits_total, repo_stat.commits_per_day, repo_stat.commits_per_week, repo_stat.commits_per_year, repo_stat.average_commit_size = await get_local_commit_stat(author_commits)
    repo_stat.using_github_features = await get_used_github_features(username, owner, repo, token)
    repo_stat.competencies = get_hardskills_from_llama(repo_path, [username, name, mail])
    
    return repo_stat

async def get_local_commit_stat(commits) -> Tuple[int, float, float, float, float]:
    """Расчет статистики коммитов из списка коммитов."""
    commit_count = 0
    total_changes = 0
    first_commit, last_commit = None, None

    # Обработка коммитов и сбор статистики
    for commit in commits:
        commit_count += 1
        commit_date = commit.committed_datetime
        total_changes += commit.stats.total['lines']

        if first_commit is None or commit_date < first_commit:
            first_commit = commit_date
        if last_commit is None or commit_date > last_commit:
            last_commit = commit_date

    if commit_count == 0:
        return 0, 0, 0, 0, 0

    # Расчеты с использованием интервала времени
    days_diff = max((last_commit - first_commit).days, 1)  # Чтобы избежать деления на ноль
    commits_per_day = commit_count / days_diff
    commits_per_week = commits_per_day * 7
    commits_per_year = commits_per_day * 365

    # Средний размер коммита
    avg_commit_size = total_changes / commit_count

    return commit_count, commits_per_day, commits_per_week, commits_per_year, avg_commit_size


async def fetch_actualize_stat(username: str, owner: str, repo: str, token: str) -> UserRepoStat:
    """
    Получение статистики репозитория из GitHub API.

    Параметры:
        username (str): Имя пользователя на GitHub.
        owner (str): Владелец репозитория.
        repo (str): Название репозитория.
        token (str): Токен доступа к GitHub API.

    Возвращает:
        UserRepoStat: Статистика репозитория.
    """
    repo_stat = await get_github_repo_stat(username, owner, repo, token)
    await create_repo_stat(repo_stat)
    return repo_stat


# Функция для получения глобальной статистики
async def fetch_global_stat(username: str, token: str) -> UserGlobalStat:
    repos = await read_repo_stat_by_username(username)
    
    global_stat = UserGlobalStat(
        username=username,
        contributed_repos=0,
        commits_total=0,
        commits_per_day=0,
        commits_per_week=0,
        commits_per_year=0,
        average_commit_size=0,
        competencies=UserCompetencyProfile(competencies={}, resume=None),  # Исправлено здесь
        using_github_features=[],
        prep_repos=[]
    )
    
    competencies = defaultdict(list)
    using_github_features = set()
    prep_repos = set()
        
    for repo in repos:
        global_stat.contributed_repos += 1
        global_stat.commits_total += repo.commits_total
        global_stat.commits_per_day += repo.commits_per_day
        global_stat.commits_per_week += repo.commits_per_week
        global_stat.commits_per_year += repo.commits_per_year
        global_stat.average_commit_size += repo.average_commit_size
        
        if repo.competencies != None:
            for category, scores in repo.competencies.competencies.items():
                competencies[category].extend(scores)
        using_github_features.update(repo.using_github_features)
        prep_repos.add(repo.repo_name)

    global_stat.competencies = UserCompetencyProfile(
        competencies=dict(competencies),
        resume=None  # Здесь можно добавить логику для объединения резюме, если это необходимо
    )
    global_stat.using_github_features = list(using_github_features)
    global_stat.prep_repos = list(prep_repos)
    
    if repos:
        global_stat.commits_per_day /= len(repos)
        global_stat.commits_per_week /= len(repos)
        global_stat.commits_per_year /= len(repos)
        global_stat.average_commit_size /= len(repos)
    
    return global_stat

# Функция для объединения профилей компетенций
async def merge_user_competency_profiles(profiles: List[UserCompetencyProfile]) -> UserCompetencyProfile:
    merged_competencies = defaultdict(list)
    resume_texts = []

    # Объединяем компетенции
    for profile in profiles:
        for category, scores in profile.competencies.items():
            merged_competencies[category].extend(scores)
        if profile.resume:
            resume_texts.append(profile.resume)

    # Создаем итоговое резюме (если нужно объединить текст)
    combined_resume = " ".join(resume_texts) if resume_texts else None

    # Возвращаем новый профиль с объединенными данными
    return UserCompetencyProfile(
        competencies=dict(merged_competencies),
        resume=combined_resume
    )

async def get_github_repo_stat(username: str, owner: str, repo: str, token: str) -> UserRepoStat:
    """
    Получение статистики репозитория из GitHub API.

    Args:
        username (str): Имя пользователя на GitHub.
        owner (str): Владелец репозитория.
        repo (str): Название репозитория.
        token (str): Токен доступа к GitHub API.

    Returns:
        UserRepoStat: Статистика репозитория.
    """
    repo_stat = UserRepoStat(
        username=username,
        repo_name=f"{owner}/{repo}",
        repo_html_url=f"https://github.com/{owner}/{repo}",
    )
    #languages, competencies, stack, score = get_competencies_by_commits(repo_commits) #TODO

    repo_commits = await get_commits(username, owner, repo, token)

    repo_stat.commits_total, repo_stat.commits_per_day, repo_stat.commits_per_week, repo_stat.commits_per_year, repo_stat.average_commit_size = await get_commit_stat(
        repo_commits
    )

    repo_stat.using_github_features = await get_used_github_features(username, owner, repo, token)

    return repo_stat


async def fetch_github_data(client: httpx.AsyncClient, url: str, params: dict = None, headers: dict = None) -> httpx.Response:
    """Формирование запроса к GitHub API."""
    response = await client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response

async def get_commits(username: str, owner: str, repo: str, token: str) -> List[dict]:
    """Получение списка коммитов пользователя."""
    all_commits = []
    current_page = 1
    commits_per_page = 100

    async with httpx.AsyncClient() as client:
        while True:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            query_params = {"author": username, "per_page": commits_per_page, "page": current_page}
            request_headers = {"Authorization": f"token {token}"}

            response = await fetch_github_data(client=client, url=api_url, params=query_params, headers=request_headers)
            if response.status_code != 200:
                break

            commits_batch = response.json()
            if not commits_batch:
                break

            for commit in commits_batch:
                commit_detail_url = commit["url"]
                commit_detail_response = await fetch_github_data(client=client, url=commit_detail_url, headers=request_headers)

                if commit_detail_response.status_code == 200:
                    commit_detail = commit_detail_response.json()
                    all_commits.append(commit_detail)

            current_page += 1

    return all_commits

async def get_used_github_features(username: str, owner: str, repo: str, token: str) -> List[str]:
    """Проверка использования различных функций GitHub."""

    feature_map = {
        "issues": await check_user_issues(owner, repo, username, token),
        "pull_requests": await check_user_pull_requests(owner, repo, username, token),
        "commits": await check_user_commits(owner, repo, username, token),
        "projects": await check_user_projects(owner, repo, username, token),
        "actions": await check_user_actions(owner, repo, username, token),
        "releases": await check_user_releases(owner, repo, username, token),
        "issue_comments": await check_user_issue_comments(owner, repo, username, token),
        "pull_request_comments": await check_user_pull_request_comments(owner, repo, username, token),
        "commit_comments": await check_user_commit_comments(owner, repo, username, token)
    }

    feature_list = [feature for feature, has_feature in feature_map.items() if has_feature]
    return feature_list

async def get_commit_stat(commits):
    """Расчет различных метрик коммитов по списку коммитов."""

    if not commits:
        return 0, 0, 0, 0, 0

    commit_count = len(commits)

    commit_dates = [
        datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S%z")
        for commit in commits
    ]

    first_commit = min(commit_dates)
    last_commit = max(commit_dates)

    days_diff = (last_commit - first_commit).days
    commits_per_day = commit_count / days_diff if days_diff > 0 else 0
    commits_per_week = commits_per_day * 7
    commits_per_year = commits_per_day * 365

    commit_sizes = [commit["stats"]["total"] for commit in commits]
    avg_commit_size = sum(commit_sizes) / len(commit_sizes)

    return commit_count, commits_per_day, commits_per_week, commits_per_year, avg_commit_size

async def get_commit_activity(username, owner, repo, token):
    # Основной URL для запросов к GitHub API
    base_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Инициализация клиента
    async with httpx.AsyncClient() as client:
        # Получение всех коммитов пользователя
        commits = []
        page = 1
        while True:
            response = await client.get(f"{base_url}?author={username}&page={page}", headers=headers)
            
            # Проверка успешности запроса
            if response.status_code != 200:
                print("Ошибка:", response.json().get("message", "Failed to fetch commits"))
                return
            
            # Получаем коммиты с текущей страницы
            data = response.json()
            if not data:  # Если коммитов больше нет
                break
            
            commits.extend(data)
            page += 1

        # Функция для получения деталей коммита асинхронно
        async def fetch_commit_details(commit):
            commit_sha = commit["sha"]
            commit_response = await client.get(f"{base_url}/{commit_sha}", headers=headers)
            
            if commit_response.status_code != 200:
                print("Ошибка:", commit_response.json().get("message", f"Failed to fetch details for commit {commit_sha}"))
                return None
            
            commit_data = commit_response.json()
            return {
                "commit_sha": commit_sha,
                "additions": commit_data["stats"]["additions"],
                "deletions": commit_data["stats"]["deletions"]
            }

        # Получаем детали каждого коммита параллельно
        commit_stats_tasks = [fetch_commit_details(commit) for commit in commits]
        commit_stats = await asyncio.gather(*commit_stats_tasks)
        
    # Фильтруем None-значения (в случае ошибок при запросе)
    return [stat for stat in commit_stats if stat is not None]

async def fetch_activity(username: str, owner:str, repo: str, token: str) -> ActivityList:
    data = await get_commit_activity(username, owner, repo, token)
    return ActivityList(
        commit_diff=[(item.get('additions') - item.get('deletions')) for item in data]
    )

