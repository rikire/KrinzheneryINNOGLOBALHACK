from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class UserRepoStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    repo_name: str = Field(..., description="Название репозитория")
    repo_html_url: str = Field(..., description="URL-адрес репозитория")
    languages: List[Dict[str, int]] = Field(..., description="Используемые языки программирования и количество строчек кода на этом языке")
    competencies: List[str] = Field(..., description="Компетенции, разработчика (направаления разработки)")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, такие как 'issues' или 'actions'")
    stack: List[str] = Field(..., description="Технологический стек, используемый в проекте (подключаемые либы)")
    score: List[Dict[str, int]] = Field(..., description="Оценки по стеку технологий (от 0 до 10)")
    commits_total: int = Field(..., description="Общее количество коммитов в репозитории")
    commits_per_day: float = Field(..., description="Среднее количество коммитов в день")
    commits_per_week: float = Field(..., description="Среднее количество коммитов в неделю")
    commits_per_year: float = Field(..., description="Среднее количество коммитов в год")
    average_commit_size: float = Field(..., description="Средний размер коммита")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "repo_name": "john_doe/sample_repo",
                "repo_html_url": "https://github.com/john_doe/sample_repo",
                "languages": [{"Python": 900}, {"HTML": 1000}],
                "competencies": ["data_analysis", "backend", "frontend", "devops"],
                "stack": ["FastAPI", "Pandas"],
                "score": [{"FastAPI": 4}, {"Pandas": 10}],
                "using_github_features": ["actions", "issues"],
                "commits_total": 150,
                "commits_per_day": 1,
                "commits_per_week": 7,
                "commits_per_year": 365,
                "average_commit_size": 100,
            }
        }


class UserGlobalStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    public_repos: int = Field(..., description="Количество публичных репозиториев")
    contributed_repos: int = Field(..., description="Количество репозиториев, к которым пользователь внес вклад")
    commits_total: int = Field(..., description="Общее количество коммитов")
    commits_per_day: float = Field(..., description="Среднее количество коммитов в день")
    commits_per_week: float = Field(..., description="Среднее количество коммитов в неделю")
    commits_per_year: float = Field(..., description="Среднее количество коммитов в год")
    average_commit_size: float = Field(..., description="Средний размер коммита")
    languages: List[Dict[str, int]] = Field(..., description="Используемые языки программирования и количество строчек кода на этом языке")
    competencies: List[str] = Field(..., description="Компетенции, разработчика (направаления разработки)")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, такие как 'issues' или 'actions'")
    stack: List[str] = Field(..., description="Технологический стек, используемый в проекте (подключаемые либы)")
    score: List[Dict[str, int]] = Field(..., description="Оценки по стеку технологий (от 0 до 10)")
    prep_repos: List[str] = Field(..., description="Список репозиториев по которым мы имеем статистику в БД")


    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "public_repos": 50,
                "contributed_repos": 20,
                "commits_total": 1000,
                "commits_per_day": 2,
                "commits_per_week": 14,
                "commits_per_year": 730,
                "average_commit_size": 120,
                "languages": [{"Python": 75}, {"JavaScript": 25}],
                "competencies": ["backend_development", "devops"],
                "using_github_features": ["pull_requests", "wiki"],
                "stack": ["Django", "Docker"],
                "score": [{"Django": 5}, {"Docker": 10}],
                "repositories":["john/repo1", "mark/repo2"]
            }
        }


class UserInfo(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    name: Optional[str] = Field(None, description="Полное имя пользователя")
    email: Optional[str] = Field(None, description="Электронная почта пользователя")
    team_projects: Optional[int] = Field(None, description="Количество проектов в команде")
    solo_projects: Optional[int] = Field(None, description="Количество личных проектов")
    solo_gist: Optional[int] = Field(None, description="Количество публичных гистов")
    account_age: Optional[int] = Field(None, description="Возраст аккаунта")
    avatar_url: Optional[str] = Field(None, description="Ссылка на аватар пользователя")
    html_url: Optional[str] = Field(None, description="Ссылка на профиль пользователя")
    followers: Optional[int] = Field(None, description="Количество подписчиков")
    following: Optional[int] = Field(None, description="Количество отслеживаемых пользователей")
    repos: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "name": "John Doe",
                "email": "john@example.com",
                "team_projects": 5,
                "solo_projects": 10,
                "solo_gist": 3,
                "account_age": 3,
                "avatar_url": "https://example.com/avatar.jpg",
                "html_url": "https://github.com/john_doe",
                "followers": 100,
                "following": 50,
                "repos:": ["jack/repo1, sparrow/repo2"]
            }
        }

class Command(BaseModel):
    command_name: str = Field(..., description="Название команды")
    participants: List[str] = Field(..., description="Участники команды")

class AccountRegister(BaseModel):
    login: str = Field(..., description="Логин аккаунта")
    password: str = Field(..., description="Пароль аккаунта")

class AccountInfo(BaseModel):
    login: str = Field(..., description="Логин аккаунта")
    command_list: List[Command] = Field(..., description="Список команд")
    favorites: List[str] = Field(..., description="Любимые разработчики")

class Summary(BaseModel):
    summary: str = Field(..., description="Описание разработчика")

class SearchResult(BaseModel):
    developers: List[UserInfo] = Field(..., description="Массив информации о пользователях")
