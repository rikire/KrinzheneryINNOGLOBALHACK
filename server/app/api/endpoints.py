from fastapi import APIRouter, status, HTTPException
from app.schemas.schema import (
    UserRepoStat, UserGlobalStat, UserInfo, SearchResult,
    AccountRegister, AccountInfo, CommandInfo, SearchQuery, ActivityList, CommandQuerry, FavoriteQuerry, FavoriteListQuerry, AccountResume, SavedUsers
)
from app.services.repo_service import (
    fetch_repo_stat, fetch_actualize_stat, fetch_global_stat, fetch_activity
)
from app.services.user_service import fetch_user_info, fetch_user_soft_skills
from app.services.search_service import fetch_search
from app.services.account_service import (
    create_acc, login_acc, update_commands, add_favorite, remove_favorite, update_favorites
)
from app.storage.crud.repo_stats import (
    delete_repo_stat
)
from app.storage.crud.users import delete_user
from app.config.config import get_token

from app.storage.storage import is_collection_empty, extract_and_save_users, get_objects_by_username, get_all_users, get_usernames_by_competency

router = APIRouter()

@router.get(
    "/saved",
    response_model=SavedUsers,
)
async def get_users():
    await extract_and_save_users()
    data = await get_all_users()
    return SavedUsers(
        users=data
    )

@router.get(
    "/find/{pattern}",
    response_model=SavedUsers,
)
async def get_sub_users(pattern: str):
    await extract_and_save_users()
    data = await get_all_users()
    data = [username for username in data if username.startswith(pattern)]
    return SavedUsers(
        users=data
    )



@router.post(
    "/competencies/{username}",
    response_model=AccountResume,
)
async def get_comps(username: str):
    
    await extract_and_save_users()
    
    user_data = await get_objects_by_username(username)

    # Формируем ответ в нужном формате
    if user_data:
        competencies_data = {}
        competencies = user_data[0].get('competencies', {})

        # Преобразуем компетенции в нужный формат
        for comp_name, comp_list in competencies.items():
            competencies_data[comp_name] = [{"name": comp['name'], "score": comp['score']} for comp in comp_list]

        resume = user_data[0].get('resume', '')

        return AccountResume(competencies=competencies_data, resume=resume)
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")



@router.get(
    "/soft_skills/{username}",
    summary="Получение софтскиллов разработчика",
    description="Возвращает список софтскиллов разработчика."
)
async def get_soft_skills(username: str):
    """
    Возвращает список софтскиллов разработчика.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.

    Returns
    -------
    Summary
        Список софтскиллов разработчика.
    """
    return await fetch_user_soft_skills(username, token=get_token())

@router.get(
    "/stat/{username}/{owner}/{repo}",
    response_model=UserRepoStat,
    summary="Получение статистики репозитория",
    description="""Возвращает статистику по конкретному репозиторию пользователя, 
    включая языки, стек технологий и метрики коммитов.
    Если есть в базе данных статистика, то возвращает ее.
    Если нет, то возвращает статистику по репозиторию с GitHub,
    предварительно клонируя его, если параметр target = 'loclal',
    или использует апи GitHub, если параметр target = 'github'.
    Затем сохраняет статистику в базу данных."""
)
async def get_repo_stat(username: str, owner: str, repo: str, target: str = 'local'):
    """
    Возвращает статистику указанного репозитория.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.
    owner : str
        Владелец репозитория.
    repo : str
        Название репозитория.
    target : str
        Источник данных 'local' или 'github'.

    Returns
    -------
    UserRepoStat
        Статистика репозитория, включая метрики и стек технологий.
    """
    return await fetch_repo_stat(username, owner, repo, token=get_token(), target=target)

@router.get(
    "/global_stat/{username}",
    response_model=UserGlobalStat,
    summary="Получение глобальной статистики пользователя",
    description="Объединяет все статистики репозиториев пользователя, которые есть в базе данных и возвращает глобальную статистику."
)
async def get_global_stat(username: str):
    """
    Возвращает глобальную статистику для пользователя на GitHub.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.

    Returns
    -------
    UserGlobalStat
        Глобальная статистика по всем репозиториям пользователя.
    """
    return await fetch_global_stat(username, token=get_token())

@router.get(
    "/user_info/{username}",
    response_model=UserInfo,
    summary="Получение информации о пользователе",
    description="Возвращает информацию о профиле пользователя на GitHub."
)
async def get_user_info(username: str):
    """
    Возвращает информацию о профиле пользователя на GitHub.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.

    Returns
    -------
    UserInfo
        Профильная информация о пользователе.
    """
    return await fetch_user_info(username, token=get_token())

@router.post(
    "/register",
    response_model=AccountInfo,
    summary="Регистрация пользователя в системе",
    description="Регистрирует нового пользователя с логином и паролем."
)
async def post_create_acc(cred: AccountRegister):
    """
    Регистрирует нового пользователя.

    Parameters
    ----------
    cred : AccountRegister
        Данные регистрации: логин и пароль.

    Returns
    -------
    AccountInfo
        Информация о созданной учетной записи.
    """
    return await create_acc(cred)

@router.post(
    "/login",
    response_model=AccountInfo,
    summary="Авторизация пользователя",
    description="Авторизует пользователя в системе с логином и паролем."
)
async def post_login_acc(cred: AccountRegister):
    """
    Авторизует пользователя.

    Parameters
    ----------
    cred : AccountRegister
        Данные для авторизации: логин и пароль.

    Returns
    -------
    AccountInfo
        Информация о учетной записи пользователя.
    """
    return await login_acc(cred)

@router.post(
    "/command",
    response_model=AccountInfo,
    summary="Добавление команды к аккаунту",
    description="Добавляет команду к учетной записи пользователя."
)
async def post_command(querry: CommandQuerry):
    """
    Изменяет команды к учетной записи пользователя.

    Parameters
    ----------
    cred : AccountRegister
        Данные для авторизации пользователя.
    command : CommandInfo
        Данные о добавляемой команде.

    Returns
    -------
    CommandInfo
        Информация о добавленной команде.
    """
    return await update_commands(querry)


@router.post(
    "/favorite",
    response_model=AccountInfo,
    summary="Добавляет пользователя в либимчики",
    description="Добавляет пользователя в либимчики"
)
async def post_add_favorite(querry: FavoriteQuerry):
    return await add_favorite(querry)

@router.post(
    "/favorite/update",
    response_model=AccountInfo,
    summary="Изменяет список любимчиков",
    description="Изменяет список любимчиков"
)
async def post_add_favorite(querry: FavoriteListQuerry):
    return await update_favorites(querry)

@router.post(
    "/favorite/delete",
    response_model=AccountInfo,
    summary="Удаляет пользователя из любимчиков",
    description="Удаляет пользователя из любимчиков"
)
async def post_add_favorite(querry: FavoriteQuerry):
    return await remove_favorite(querry)

@router.post(
    "/search",
    response_model=SavedUsers,
    summary="Поиск пользователей по компетенциям",
    description="Ищет пользователей на основе заданных компетенций и возвращает список профилей."
)
async def get_search(search_query: SearchQuery):
    """
    Ищет пользователей по компетенциям.

    Parameters
    ----------
    search_query : SearchQuery
        Запрос с параметрами для поиска пользователей.

    Returns
    -------
    SearchResult
        Список найденных пользователей, соответствующих запросу.
    """
    await extract_and_save_users()
    query = search_query.query
    users = await get_usernames_by_competency(query)
    return SavedUsers(
        users=users
    )

@router.get(
    "/activity/{username}/{owner}/{repo}",
    response_model=ActivityList,
    summary="Получение числовых характеристик коммитов",
    description="Возвращает числовые характеристики изменений коммитов в указанном репозитории."
)
async def get_activity(username: str, owner: str, repo: str):
    """
    Возвращает числовые характеристики изменений коммитов.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.
    owner : str
        Владелец репозитория.
    repo : str
        Название репозитория.

    Returns
    -------
    ActivityList
        Список разностей между добавленными и удаленными строками коммитов.
    """
    return await fetch_activity(username, owner, repo, get_token())

@router.delete(
    "/delete_stat/{username}/{owner}/{repo}",
    summary="Удаление статистики репозитория из БД",
    description="Удаляет статистику репозитория из БД."
)
async def delete_repo(username: str, owner: str, repo: str):
    """
    Удаляет статистику репозитория из БД.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.
    owner : str
        Владелец репозитория.
    repo : str
        Название репозитория.

    Returns
    -------
    UserRepoStat
        Удаленная статистика репозитория.
    """
    return await delete_repo_stat(username, f"{owner}/{repo}")


@router.delete(
    "/delete_user_info/{username}",
    summary="Удаление информации о пользователе из БД",
    description="Удаляет информацию о пользователе из БД."
)
async def delete_user_info(username: str):
    """
    Удаляет информацию о пользователе из БД.

    Parameters
    ----------
    username : str
        Имя пользователя на GitHub.

    Returns
    -------
    UserInfo
        Удаленная информация о пользователе.
    """
    res = await delete_user(username)
    if res != None:
        return status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND