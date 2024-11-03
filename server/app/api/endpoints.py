from fastapi import APIRouter
from app.schemas.schema import UserRepoStat, UserGlobalStat, UserInfo, Summary, SearchResult, AccountRegister, AccountInfo, CommandInfo, SearchQuery, ActivityList

from app.services.repo_service import fetch_repo_stat, fetch_actualize_stat, fetch_global_stat, fetch_activity
from app.services.user_service import fetch_user_info
from app.services.search_service import fetch_search
from app.services.account_service import create_acc, login_acc, add_command, remove_command

import yaml


router = APIRouter()

def get_token():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config.get("github_token")

@router.get(
    "/stat/{username}/{owner}/{repo}",
    response_model=UserRepoStat,
    summary="Получение статистики репозитория",
    description="Возвращает статистику по конкретному репозиторию пользователя, включая языки, стек технологий и метрики коммитов.",
)
async def get_repo_stat(username: str, owner: str, repo: str, target: str = 'github'):
    """
    Обновляет информацию о статистике репозитория в бд.

    - **username**: Имя пользователя на GitHub
    - **owner**: Владелец репозитория
    - **repo**: Название репозитория
    """
    return await fetch_repo_stat(username, owner, repo, token=get_token(), target=target)

@router.get(
    "/actualize_stat/{username}/{owner}/{repo}",
    response_model=UserRepoStat,
    summary="Актуализация статистики репозитория",
    description="Обновляет информацию о статистике репозитория в бд."
)
async def get_actualize_stat(username: str, owner: str, repo: str):
    """
    Обновляет информацию о статистике репозитория в бд.

    - **username**: Имя пользователя на GitHub
    - **owner**: Владелец репозитория
    - **repo**: Название репозитория
    """
    return await fetch_actualize_stat(username, owner, repo, token=get_token())

@router.get(
    "/global_stat/{username}",
    response_model=UserGlobalStat,
    summary="Возвращает глобальную статистику о пользователе",
    description="Сканирует все репозитории человека и возвращает глобальную статистику."
)
async def get_global_stat(username: str):
    """
    Возвращает глобальную статистику о пользователе.

    - **username**: Имя пользователя на GitHub
    """
    return await fetch_global_stat(username, token=get_token())

@router.get(
    "/user_info/{username}",
    response_model=UserInfo,
    summary="Возвращает информацию о пользователе",
    description="Возвращает информацию о профиле пользователя на гитхаб."
)
async def get_user_info(username: str):
    """
    Возвращает информацию о профиле пользователя на гитхаб.

    - **username**: Имя пользователя на GitHub
    """
    return await fetch_user_info(username, token=get_token())

@router.post(
    "/register",
    response_model=AccountInfo,
    summary="Регестрирует пользователя в системе",
    description="Принимает логин и пароль.")
async def post_create_acc(cred: AccountRegister):
    return await create_acc(cred)

# Гет для комманд -_-
@router.post(
    "/login",
    response_model=AccountInfo,
    summary="Авторизирует пользователя в системе",
    description="Принимает логин и пароль.")
async def post_login_acc(cred: AccountRegister):
    return await login_acc(cred)


@router.post(
    "/command",
    response_model=CommandInfo,
    summary="Добавить команду к аккаунтую",
    description="Добавить команду к аккаунту.")
async def post_command(cred: AccountRegister, command: CommandInfo):
    return await add_command(cred, command)

@router.post("/command/delete",
    response_model=CommandInfo,
    summary="Убрать команду из аккаунта",
    description="Убрать команду из аккаунта.")
async def post_command_del(cred: AccountRegister, command: CommandInfo):
    return await remove_command(cred, command)

@router.post(
    "/search",
    response_model=SearchResult,
    summary="Поиск пользователей по компетенциям",
    description="Возвращает список UserInfo."
)
async def get_search(search_query: SearchQuery):
    query = search_query.query
    return await fetch_search(query, token=get_token())

@router.get(
    "/activity/{username}/{owner}/{repo}",
    response_model=ActivityList,
    summary="Получение числовых характеристик изменения коммитов.",
    description="Получение числовых характеристик изменения коммитов.")
async def get_activity(username: str, owner: str, repo: str):
    return await fetch_activity(username, owner, repo, get_token())

@router.post(
    "/post_analysis/{username}/{owner}/{repo}",
    summary="Получение анализа от llama",
    description="Получение анализа от llama."
)
async def post_analysis(username: str, owner: str, repo: str):
    return await fetch_analysis(username, owner, repo, get_token())