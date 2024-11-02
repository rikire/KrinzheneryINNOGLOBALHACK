from fastapi import APIRouter
from app.schemas.schema import UserRepoStat, UserGlobalStat, UserInfo, Summary, SearchResult, AccountRegister, AccountInfo, Command
from app.services.repo_service import fetch_repo_stat
router = APIRouter()

def get_token():
    return "TOKEN"

@router.get(
    "/stat/{username}/{owner}/{repo}",
    response_model=UserRepoStat,
    summary="Получение статистики репозитория",
    description="Возвращает статистику по конкретному репозиторию пользователя, включая языки, стек технологий и метрики коммитов.",
)
async def get_repo_stat(username: str, owner: str, repo: str):
    """
    Обновляет информацию о статистике репозитория в бд.

    - **username**: Имя пользователя на GitHub
    - **owner**: Владелец репозитория
    - **repo**: Название репозитория
    """
    return await fetch_repo_stat(username, owner, repo, token=get_token())

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

@router.get(
    "/summary/{username}",
    response_model=Summary,
    summary="Возвращает саммари о пользователе",
    description="Возвращает саммари о пользователе, сгенерированное ламой."
)
async def get_summary(username: str):
    """
    Возвращает саммари о пользователе, сгенерированное ламой.

    - **username**: Имя пользователя на GitHub
    """
    return await fetch_summary(username, token=get_token())

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
    summary="CRUD для комманд.",
    description="Принимает комманду.")
async def post_command(cred: AccountRegister, command: Command):
    return await crud_command(cred, command)

@router.post("/command/delete")
async def post_command_del(cred: AccountRegister, command: Command):
    return await post_command_del(cred, command)

@router.get(
    "/search/{querry}",
    response_model=SearchResult,
    summary="Поиск пользователей по компетенциям",
    description="Возвращает список UserInfo.")
async def get_search(querry: str):
    return await fetch_search(querry)
