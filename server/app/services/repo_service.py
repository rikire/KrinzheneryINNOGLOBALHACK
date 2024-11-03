from app.storage.crud.repo_stats import read_repo_stat_by_username, read_repo_stat, repo_stat_exists, create_repo_stat
from app.models.models import RepoStat
from app.schemas.schema import UserGlobalStat
from app.services.github_utils import check_user_actions, check_user_projects, check_user_commit_comments, check_user_commits, check_user_issues, check_user_issue_comments, check_user_pull_request_comments, check_user_pull_requests, check_user_releases

import git
import asyncio
import httpx
from typing import List, Dict, Tuple
import datetime

async def fetch_repo_stat(username: str, owner: str, repo: str, token: str, target: str) -> RepoStat:
    """
    Retrieve a repository's statistics from the cache or GitHub API.

    Args:
        username (str): The username of the repository owner.
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str): The GitHub API access token.

    Returns:
        RepoStat: The repository's statistics.
    """
    repo_name = f"{owner}/{repo}"
    if await repo_stat_exists(username, repo_name):
        return await read_repo_stat(username, repo_name)
    if target == 'local':
        repo_stat = await get_local_repo_stat(username, owner, repo, token)
        await create_repo_stat(repo_stat)
    if target == 'github':
        repo_stat = await get_github_repo_stat(username, owner, repo, token)
        await create_repo_stat(repo_stat)
    return repo_stat

async def get_local_repo_stat(username: str, owner: str, repo: str, token: str) -> RepoStat:
    """
    Retrieve a repository's statistics from the local Git repository.

    Args:
        username (str): The username of the repository owner.
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str): The GitHub API access token (not used here).

    Returns:
        RepoStat: The repository's statistics.
    """
    repo_stat = RepoStat(
        username=username,
        repo_name=f"{owner}/{repo}",
        repo_html_url=f"https://github.com/{owner}/{repo}",
        languages=[],
        competencies=[],
        using_github_features=[],
        stack=[],
        score=[],
        commits_total=0,
        commits_per_day=0,
        commits_per_week=0,
        commits_per_year=0,
        average_commit_size=0
    )

    local_repo = None
    repo_path = f"./dataset/{repo}"
    try:
        local_repo = git.Repo(repo_path)
    except git.exc.NoSuchPathError:
        gitclone = git.Repo.clone_from(f"https://github.com/{owner}/{repo}.git", repo_path)
        if gitclone is None:
            raise Exception(f"Failed to clone repository {owner}/{repo}.")
        local_repo = git.Repo(repo_path)
    
    # Fetch the author’s commits
    # name, mail, username
    author_commits = local_repo.iter_commits(author=username)

    # Calculate commit statistics
    repo_stat.commits_total, repo_stat.commits_per_day, repo_stat.commits_per_week, repo_stat.commits_per_year, repo_stat.average_commit_size = await get_local_commit_stat(author_commits)
    repo_stat.using_github_features = await get_used_github_features(username, owner, repo, token)
    
    return repo_stat

async def get_local_commit_stat(commits) -> Tuple[int, float, float, float, float]:
    """Calculate various commit statistics from a list of commits."""
    commit_count = 0
    total_changes = 0
    first_commit, last_commit = None, None

    # Process commits and gather stats
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

    # Time range calculations
    days_diff = max((last_commit - first_commit).days, 1)  # Avoid division by zero
    commits_per_day = commit_count / days_diff
    commits_per_week = commits_per_day * 7
    commits_per_year = commits_per_day * 365

    # Average commit size
    avg_commit_size = total_changes / commit_count

    return commit_count, commits_per_day, commits_per_week, commits_per_year, avg_commit_size


async def fetch_actualize_stat(username: str, owner: str, repo: str, token: str) -> RepoStat:
    """
    Retrieve a repository's statistics from the GitHub API.

    Args:
        username (str): The username of the repository owner.
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str): The GitHub API access token.

    Returns:
        RepoStat: The repository's statistics.
    """
    repo_stat = await get_github_repo_stat(username, owner, repo, token)
    await create_repo_stat(repo_stat)
    return repo_stat
    
async def fetch_global_stat(username: str, token: str) -> UserGlobalStat:
    repos = await read_repo_stat_by_username(username)
    
    global_stat = UserGlobalStat(
        username=username,
        public_repos=0,
        contributed_repos=0,
        commits_total=0,
        commits_per_day=0,
        commits_per_week=0,
        commits_per_year=0,
        average_commit_size=0,
        languages=[],
        competencies=[],
        using_github_features=[],
        stack=[],
        score=[],
        prep_repos=[]
    )
    
    languages=set()
    competencies=set()
    using_github_features=set()
    stack=set()
    score=set()
    
    for repo in repos:
        global_stat.public_repos += 1
        if username.lower() in repo.repo_name.lower():
            global_stat.public_repos += 1
        global_stat.commits_total += repo.commits_total
        global_stat.commits_per_day += repo.commits_per_day
        global_stat.commits_per_week += repo.commits_per_week
        global_stat.commits_per_year += repo.commits_per_year
        global_stat.average_commit_size += repo.average_commit_size
        languages.update(repo.languages)
        competencies.update(repo.competencies)
        using_github_features.update(repo.using_github_features)
        stack.update(repo.stack)
        score.update(repo.score)
        global_stat.prep_repos.append(repo.repo_name)

    global_stat.languages = list(languages)
    global_stat.competencies = list(competencies)
    global_stat.using_github_features = list(using_github_features)
    global_stat.stack = list(stack)
    global_stat.score = list(score)
    
    global_stat.commits_per_day /= len(repos)
    global_stat.commits_per_week /= len(repos)
    global_stat.commits_per_year /= len(repos)
    global_stat.average_commit_size /= len(repos)
    
    return global_stat
    
async def get_github_repo_stat(username: str, owner: str, repo: str, token: str) -> RepoStat:
    """
    Retrieve a repository's statistics from the GitHub API.

    Args:
        username (str): The username of the repository owner.
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str): The GitHub API access token.

    Returns:
        RepoStat: The repository's statistics.
    """
    repo_stat = RepoStat(
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
    """Fetch data from the GitHub API."""
    response = await client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response

async def get_commits(username: str, owner: str, repo: str, token: str) -> List[dict]:
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
    """Calculate various commit statistics from a list of commits."""
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

