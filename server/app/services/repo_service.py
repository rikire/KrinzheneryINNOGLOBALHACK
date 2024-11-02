from app.storage.crud.repo_stats import read_repo_stat, is_repo_stat_exists, create_repo_stat
from app.models.models import RepoStat
import asyncio
import httpx
from typing import List, Dict
import datetime

async def fetch_repo_stat(username: str, owner: str, repo: str, token: str):
    repo_name = f"{owner}/{repo}"
    if await is_repo_stat_exists(username, repo_name):
        return await read_repo_stat(username, repo_name)
    else:
        repo_stat = await get_github_repo_stat(username, owner, repo, token)
        create_repo_stat(repo_stat)
        return repo_stat
    
async def get_github_repo_stat(username: str, owner: str, repo: str, token: str) -> RepoStat:
    repo_stat = RepoStat(
        username=username,
        repo_name=f"{owner}/{repo}",
        repo_html_url=f"https://github.com/{owner}/{repo}"
    )
    
    #languages, competencies, stack, score = get_competencies_by_commits(repo_commits) #TODO
    
    repo_stat.languages = [] # TODO
    repo_stat.competencies = [] # TODO
    repo_stat.stack = [] # TODO
    repo_stat.score = [] # TODO

    repo_stat.using_github_features = await get_using_github_features(username, owner, repo, token) # TODO

    repo_commits = await get_commits(username, owner, repo, token)
    
    repo_stat.commits_total, repo_stat.commits_per_day, repo_stat.commits_per_week, repo_stat.commits_per_year, repo_stat.average_commit_size = await get_commit_stat(repo_commits)
    
    return repo_stat

async def fetch_github_data(client: httpx.AsyncClient, url: str, params: dict = None, headers: dict = None) -> httpx.Response:
    response = await client.get(url, params=params, headers=headers)
    return response

async def get_commits(username: str, owner: str, repo: str, token: str) -> List[dict]:
    commits = []
    page = 1
    per_page = 100

    async with httpx.AsyncClient() as client:
        while True:
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            params = {"author": username, "per_page": per_page, "page": page}
            headers = {"Authorization": f"token {token}"}

            response = await fetch_github_data(client=client, url=url, params=params, headers=headers)
            if response.status_code == 200:
                commit_data = response.json()
                if not commit_data:
                    break
                for commit in commit_data:
                    commit_url = commit["url"]
                    commit_response = await fetch_github_data(client=client, url=commit_url, headers=headers)
                    if commit_response.status_code == 200:
                        commit_detail = commit_response.json()
                        commits.append(commit_detail)
                page += 1
            else:
                break

    return commits

async def get_using_github_features(username: str, owner: str, repo: str, token: str) -> List[str]:
    features_keys = ["issues", "pull_requests", "commits", "discussions", "projects", "wiki", "actions", "releases"]
    features = {key: False for key in features_keys}

    urls = {
        "issues": f"https://api.github.com/repos/{owner}/{repo}/issues",
        "pull_requests": f"https://api.github.com/repos/{owner}/{repo}/pulls",
        "commits": f"https://api.github.com/repos/{owner}/{repo}/commits",
        "discussions": f"https://api.github.com/repos/{owner}/{repo}/discussions",
        "projects": f"https://api.github.com/repos/{owner}/{repo}/projects",
        "wiki": f"https://api.github.com/repos/{owner}/{repo}/wiki",
        "actions": f"https://api.github.com/repos/{owner}/{repo}/actions",
        "releases": f"https://api.github.com/repos/{owner}/{repo}/releases",
    }
    header = {"Authorization": f"token {token}"}
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(
            *(fetch_github_data(client=client, url=url, headers=header) for url in urls.values())
        )
        for response, feature_key in zip(responses, features_keys):
            if response.status_code == 200:
                data = response.json()
                if data:
                    match feature_key:
                        case "issues":
                            for issue in data:
                                if issue["user"]["login"].lower() == username.lower():
                                    features["issues"] = True
                                    
                        case "pull_requests":
                            for pull_request in data:
                                if pull_request["user"]["login"].lower() == username.lower():
                                    features["pull_requests"] = True

                        case "commits":
                            for commit in data:
                                if commit["author"]["name"].lower() == username.lower():
                                    features["commits"] = True
                                    
                        case "discussions": #TODO
                            for discussion in data:
                                if discussion["user"]["login"].lower() == username.lower():
                                    features["discussions"] = True

                        case "projects": #TODO
                            for project in data:
                                if project["user"]["login"].lower() == username.lower():
                                    features["projects"] = True

                        case "wiki": #TODO
                            for wiki in data:
                                if wiki["user"]["login"].lower() == username.lower():
                                    features["wiki"] = True

                        case "actions": #TODO
                            for action in data:
                                if action["user"]["login"].lower() == username.lower():
                                    features["actions"] = True

                        case "releases": #TODO
                            for release in data:
                                if release["author"]["login"].lower() == username.lower():
                                    features["releases"] = True
                        case _:
                            features[feature_key] = False
    
    return [feature for feature in features if features[feature]]

async def get_commit_stat(commits):
    if not commits:
        return 0, 0, 0, 0, 0

    total_commits = len(commits)

    commit_dates = [
        datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S%z")
        for commit in commits
    ]

    first_commit_date = min(commit_dates)
    last_commit_date = max(commit_dates)

    days_diff = (last_commit_date - first_commit_date).days
    commits_per_day = total_commits / days_diff if days_diff > 0 else 0
    commits_per_week = commits_per_day * 7
    commits_per_year = commits_per_day * 365

    commit_sizes = [
        commit["stats"]["total"]
        for commit in commits
        ]
    
    average_commit_size = sum(commit_sizes) / len(commit_sizes)

    return total_commits, commits_per_day, commits_per_week, commits_per_year, average_commit_size
