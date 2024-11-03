from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Score(BaseModel):
    name: str = Field(..., description="Название компетенции")
    score: int = Field(..., description="Оценка по компетенции")

class Competence(BaseModel):
    competence: List[Score] = Field(..., description="Список оценок по компетенциям")

class Competencies(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    repo_name: str = Field(..., description="Название репозитория в формате '{owner}/{repo}'")
    competencies: List[Competence] = Field(..., description="Список компетенций разработчика")
    resume: str = Field(..., description="Резюме разработчика")

class UserRepoStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    repo_name: str = Field(..., description="Название репозитория в формате '{owner}/{repo}'")
    repo_html_url: str = Field(..., description="URL-адрес репозитория")
    competencies: List[Competencies] = Field(..., description="Список компетенций разработчика")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, такие как 'issues' или 'actions'")
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
                "competencies": [
                    {
                        "username": "john_doe",
                        "repo_name": "john_doe/sample_repo",
                        "competencies": [{"competence": [{"name": "FastAPI", "score": 4}, {"name": "Pandas", "score": 10}]}],
                        "resume": "Backend developer with expertise in Python"
                    }
                ],
                "using_github_features": ["actions", "issues"],
                "commits_total": 150,
                "commits_per_day": 1.5,
                "commits_per_week": 10.5,
                "commits_per_year": 365,
                "average_commit_size": 120.5,
            }
        }

class UserGlobalStat(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    contributed_repos: int = Field(..., description="Количество репозиториев, к которым пользователь внес вклад")
    commits_total: int = Field(..., description="Общее количество коммитов")
    commits_per_day: float = Field(..., description="Среднее количество коммитов в день")
    commits_per_week: float = Field(..., description="Среднее количество коммитов в неделю")
    commits_per_year: float = Field(..., description="Среднее количество коммитов в год")
    average_commit_size: float = Field(..., description="Средний размер коммита")
    competencies: List[Competencies] = Field(..., description="Список компетенций разработчика")
    using_github_features: List[str] = Field(..., description="Используемые функции GitHub, такие как 'issues' или 'actions'")
    prep_repos: List[str] = Field(..., description="Список репозиториев, по которым имеется статистика в БД")

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
                "competencies": [
                    {
                        "username": "john_doe",
                        "repo_name": "john_doe/sample_repo",
                        "competencies": [{"competence": [{"name": "Django", "score": 8}, {"name": "Docker", "score": 7}]}],
                        "resume": "Experienced developer in backend and DevOps"
                    }
                ],
                "using_github_features": ["pull_requests", "wiki"],
                "prep_repos": ["john_doe/repo1", "mark/repo2"]
            }
        }

class UserInfo(BaseModel):
    username: str = Field(..., description="Имя пользователя на GitHub")
    name: Optional[str] = Field(None, description="Полное имя пользователя")
    email: Optional[str] = Field(None, description="Электронная почта пользователя")
    team_projects: Optional[int] = Field(None, description="Количество проектов в команде")
    solo_projects: Optional[int] = Field(None, description="Количество личных проектов")
    solo_gist: Optional[int] = Field(None, description="Количество публичных гистов")
    account_age: Optional[int] = Field(None, description="Возраст аккаунта в годах")
    avatar_url: Optional[str] = Field(None, description="Ссылка на аватар пользователя")
    html_url: Optional[str] = Field(None, description="Ссылка на профиль пользователя")
    followers: Optional[int] = Field(None, description="Количество подписчиков")
    following: Optional[int] = Field(None, description="Количество отслеживаемых пользователей")
    repos: List[str] = Field(..., description="Список репозиториев, в которые пользователь контрибьютил, в формате '{owner}/{repo}'")

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
    participants: List[str] = Field(..., description="Участники команды")

class AccountRegister(BaseModel):
    login: str = Field(..., description="Логин аккаунта")
    password: str = Field(..., description="Пароль аккаунта")

class AccountInfo(BaseModel):
    login: str = Field(..., description="Логин аккаунта")
    command_list: List[CommandInfo] = Field(..., description="Список команд")
    favorites: List[str] = Field(..., description="Любимые разработчики")

class Summary(BaseModel):
    summary: str = Field(..., description="Описание разработчика")

class SearchQuery(BaseModel):
    query: str = Field(..., description="Строка запроса для поиска пользователей по компетенциям.")

class SearchResult(BaseModel):
    developers: List[UserInfo] = Field(..., description="Массив информации о пользователях")

class ActivityList(BaseModel):
    commit_diff: List[int] = Field(..., description="Список разностей между добавленными и удаленными строками коммитов")
