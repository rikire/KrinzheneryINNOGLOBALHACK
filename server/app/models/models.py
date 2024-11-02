from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class UserInfo(BaseModel):
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    team_projects: Optional[int] = None
    solo_projects: Optional[int] = None
    solo_gist: Optional[int] = None
    account_age: Optional[int] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    repos: List[str] = Field(default_factory=list)


class RepoStat(BaseModel):
    username: str
    repo_name: str
    repo_html_url: str
    languages: List[Dict[str, int]] = Field(default_factory=list)
    competencies: List[str] = Field(default_factory=list)
    using_github_features: List[str] = Field(default_factory=list)
    stack: List[str] = Field(default_factory=list)
    score: List[Dict[str, int]] = Field(default_factory=list)
    commits_total: Optional[int] = None
    commits_per_day: Optional[float] = None
    commits_per_week: Optional[float] = None
    commits_per_year: Optional[float] = None
    average_commit_size: Optional[float] = None


class Command(BaseModel):
    command_name: Optional[str] = None
    participants: List[str] = Field(default_factory=list)


class Account(BaseModel):
    login: str
    password: str
    command_list: List[Command] = Field(default_factory=list)
    favorites: List[str] = Field(default_factory=list)


class Summary(BaseModel):
    username: str
    summary: str
