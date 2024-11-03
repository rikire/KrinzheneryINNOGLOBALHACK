from pydantic import BaseModel, Field 
from typing import Optional, List, Dict
from datetime import datetime


class Score(BaseModel):
    name: str = Field(..., description="Название компетенции")
    score: int = Field(..., description="Оценка (0-10)")

class UserCompetencyProfile(BaseModel):
    competencies: Optional[Dict[str, List[Score]]] = Field(None, description="Категории и соответствующие компетенции с оценками")
    resume: Optional[str] = Field(None, description="Описание компетенций пользователя")
    
    class Config:
        json_schema_extra = {
            "example": {
                "competencies": {
                    "frontend": [{"name": "SVG", "score": 8}],
                    "backend": [{"name": "go", "score": 9}, {"name": "ruby", "score": 6}],
                    "devops": [{"name": "Docker", "score": 8}],
                    "other": [{"name": "bash", "score": 8}]
                },
                "resume": "Эксперт в контейнеризации и виртуализации."
            }
        }

class UserRepoStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    repo_name: str = Field(..., description="Репозиторий в формате '{owner}/{repo}'")
    repo_html_url: str = Field(..., description="URL репозитория")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, напр. 'issues'")
    commits_total: int = Field(..., description="Общее количество коммитов")
    commits_per_day: float = Field(..., description="Среднее коммитов в день")
    commits_per_week: float = Field(..., description="Среднее коммитов в неделю")
    commits_per_year: float = Field(..., description="Среднее коммитов в год")
    average_commit_size: float = Field(..., description="Средний размер коммита")
    competencies: Optional[UserCompetencyProfile] = Field(None, description="Компетенции разработчика")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "repo_name": "john_doe/sample_repo",
                "repo_html_url": "https://github.com/john_doe/sample_repo",
                "competencies": {
                    "frontend": [{"name": "SVG", "score": 8}],
                    "backend": [{"name": "FastAPI", "score": 4}],
                    "resume": "Backend developer with expertise in Python"
                },
                "using_github_features": ["actions", "issues"],
                "commits_total": 150,
                "commits_per_day": 1.5,
                "commits_per_week": 10.5,
                "commits_per_year": 365,
                "average_commit_size": 120.5
            }
        }

class UserGlobalStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    contributed_repos: int = Field(..., description="Число репозиториев, к которым внесены вклады")
    commits_total: int = Field(..., description="Общее количество коммитов")
    commits_per_day: float = Field(..., description="Среднее коммитов в день")
    commits_per_week: float = Field(..., description="Среднее коммитов в неделю")
    commits_per_year: float = Field(..., description="Среднее коммитов в год")
    average_commit_size: float = Field(..., description="Средний размер коммита")
    competencies: UserCompetencyProfile = Field(..., description="Компетенции пользователя")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, напр. 'pull_requests'")
    prep_repos: List[str] = Field(..., description="Список репозиториев со статистикой в БД")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "contributed_repos": 20,
                "commits_total": 1000,
                "commits_per_day": 2.5,
                "commits_per_week": 17.5,
                "commits_per_year": 910,
                "average_commit_size": 115.0,
                "competencies": {
                    "backend": [{"name": "Django", "score": 8}],
                    "devops": [{"name": "Docker", "score": 7}],
                    "resume": "Experienced in backend and DevOps"
                },
                "using_github_features": ["pull_requests", "wiki"],
                "prep_repos": ["john_doe/repo1", "mark/repo2"]
            }
        }

class UserInfo(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    name: Optional[str] = Field(None, description="Полное имя")
    email: Optional[str] = Field(None, description="Электронная почта")
    team_projects: Optional[int] = Field(None, description="Количество командных проектов")
    solo_projects: Optional[int] = Field(None, description="Количество личных проектов")
    solo_gist: Optional[int] = Field(None, description="Количество публичных гистов")
    account_age: Optional[int] = Field(None, description="Возраст аккаунта в годах")
    avatar_url: Optional[str] = Field(None, description="Ссылка на аватар")
    html_url: Optional[str] = Field(None, description="Ссылка на профиль")
    followers: Optional[int] = Field(None, description="Количество подписчиков")
    following: Optional[int] = Field(None, description="Число отслеживаемых пользователей")
    repos: List[str] = Field(..., description="Список репозиториев в формате '{owner}/{repo}'")

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
                "repos": ["jack/repo1", "sparrow/repo2"]
            }
        }

class CommandInfo(BaseModel):
    command_name: str = Field(..., description="Название команды")
    participants: List[str] = Field(..., description="Список участников")

class AccountRegister(BaseModel):
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")

class AccountInfo(BaseModel):
    login: str = Field(..., description="Логин")
    command_list: List[CommandInfo] = Field(..., description="Список команд")
    favorites: List[str] = Field(..., description="Избранные разработчики")

class Summary(BaseModel):
    summary: str = Field(..., description="Описание разработчика")

class SearchQuery(BaseModel):
    query: str = Field(..., description="Запрос для поиска пользователей по компетенциям")

class SearchResult(BaseModel):
    developers: List[UserInfo] = Field(..., description="Информация о найденных пользователях")

class CommitInfo(BaseModel):
    additions: int = Field(..., description="Добавленные строки")
    deletions: int = Field(..., description="Удаленные строки")
    commit_date: datetime = Field(..., description="Дата коммита")
    commit_message: str = Field(..., description="Сообщение коммита")

class ActivityList(BaseModel):
    commits: List[CommitInfo] = Field(..., description="Описания коммитов")

class CommandQuerry(BaseModel):
    login: str = Field(..., description="Логин")
    command: CommandInfo = Field(..., description="Команда")