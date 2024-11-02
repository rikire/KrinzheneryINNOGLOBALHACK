from app.storage.crud.repo_stats import read_repo_stat, repo_stat_exists, create_repo_stat
from app.models.models import RepoStat
import asyncio
import httpx
from typing import List, Dict
import datetime

async def fetch_repo_stat(username: str, owner: str, repo: str, token: str) -> RepoStat:
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
    repo_stat = await get_github_repo_stat(username, owner, repo, token)
    await create_repo_stat(repo_stat)
    return repo_stat
    
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
    """Fetches a list of GitHub features used by the given username in the given repo."""

    features = {
        "issues": False,
        "pull_requests": False,
        "commits": False,
        "discussions": False,
        "projects": False,
        "wiki": False,
        "actions": False,
        "releases": False,
    }

    urls = {
        "issues": f"https://api.github.com/repos/{owner}/{repo}/issues",
        "pull_requests": f"https://api.github.com/repos/{owner}/{repo}/pulls",
        "commits": f"https://api.github.com/repos/{owner}/{repo}/commits",
        "discussions": f"https://api.github.com/repos/{owner}/{repo}/discussions",
        "projects": f"https://api.github.com/repos/{owner}/{repo}/projects",
        "actions": f"https://api.github.com/repos/{owner}/{repo}/actions",
        "releases": f"https://api.github.com/repos/{owner}/{repo}/releases",
    }

    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(
            *(fetch_github_data(client=client, url=url, headers={"Authorization": f"token {token}"}) for url in urls.values()),
            return_exceptions=True,
        )
        for response, feature_key in zip(responses, features.keys()):
            if isinstance(response, Exception):
                continue
            if response.status_code != 200:
                continue

            data = response.json()
            if not data:
                continue

            # Check if the username is associated with each feature
            match feature_key:
                case "issues" | "pull_requests" | "discussions" | "projects" | "releases":
                    for item in data:
                        if item.get("user", {}).get("login", "").lower() == username.lower():
                            features[feature_key] = True
                            break
                case "commits":
                    for commit in data:
                        if commit.get("author", {}).get("name", "").lower() == username.lower():
                            features["commits"] = True
                            break
                case "actions":
                    features["actions"] = bool(data)

    return [feature for feature, used in features.items() if used]

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

