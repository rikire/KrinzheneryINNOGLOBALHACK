from app.schemas.schema import AccountInfo, AccountRegister, CommandInfo, CommandQuerry, FavoriteQuerry, FavoriteListQuerry
from app.models.models import Account, Command
from app.storage.crud.accounts import create_account, get_account, update_account


async def create_acc(cred : AccountRegister) -> AccountInfo:
    acc = Account(
        login=cred.login,
        password=cred.password,
        command_list=[],
        favorites=[]
    )
    acc = await create_account(acc)
    return AccountInfo(
        login=cred.login,
        password=cred.password,
        command_list=[],
        favorites=[]
    )

def command_to_info(command: Command):
    return CommandInfo(
        command_name=command.command_name,
        participants=command.participants
    )

async def login_acc(cred: AccountRegister) -> AccountInfo:
    acc = await get_account(cred.login)
    if acc is None or acc.password != cred.password:
        return None
    else:
        return AccountInfo(
        login=acc.login,
        password=acc.password,
        command_list=[command_to_info(item) for item in acc.command_list],
        favorites=acc.favorites
    )

async def update_commands(querry: CommandQuerry):
    commands = [Command(
        command_name = com.command_name,
        participants = com.participants
    ) for com in querry.commands]
    acc = await get_account(querry.login)
    if acc is None:
        return None
    else:
        acc.command_list=commands
        await update_account(querry.login, acc)
        return AccountInfo(
            login=acc.login,
            command_list=[command_to_info(item) for item in acc.command_list],
            favorites=acc.favorites
        )
    

async def update_favorites(querry: FavoriteListQuerry):
    acc = await get_account(querry.login)
    if acc is None:
        return None
    else:
        acc.favorites = querry.favorites
        await update_account(querry.login, acc)
        return AccountInfo(
            login=acc.login,
            command_list=[command_to_info(item) for item in acc.command_list],
            favorites=acc.favorites
        )

async def add_favorite(querry: FavoriteQuerry):
    acc = await get_account(querry.login)
    if acc is None:
        return None
    else:
        acc.favorites.append(querry.target)
        await update_account(querry.login, acc)
        return AccountInfo(
            login=acc.login,
            command_list=[command_to_info(item) for item in acc.command_list],
            favorites=acc.favorites
        )

async def remove_favorite(querry: FavoriteQuerry):
    acc = await get_account(querry.login)
    if acc is None:
        return None
    else:
        acc.favorites.remove(querry.target)
        await update_account(querry.login, acc)
        return AccountInfo(
            login=acc.login,
            command_list=[command_to_info(item) for item in acc.command_list],
            favorites=acc.favorites
        )

async def add_account(querry: FavoriteQuerry):
    acc = await get_account(querry.login)
    if acc is None:
        return None
    else:
        acc.favorites.append(querry.target)
        await update_account(querry.login, acc)
        return AccountInfo(
            login=acc.login,
            command_list=[command_to_info(item) for item in acc.command_list],
            favorites=acc.favorites
        )
            