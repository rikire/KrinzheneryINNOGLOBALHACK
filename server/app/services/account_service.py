from app.schemas.schema import AccountInfo, AccountRegister, CommandInfo
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

async def login_acc(cred: AccountRegister) -> AccountInfo:
    acc = await get_account(cred.login)
    if acc is None or acc.password != cred.password:
        return None
    else:
        return AccountInfo(
        login=acc.login,
        password=acc.password,
        command_list=acc.command_list,
        favorites=acc.favorites
    )

async def add_command(cred: AccountRegister, command: CommandInfo):
    command_obj = Command(
        command_name = command.command_name,
        participants = command.participants
    )
    acc = await get_account(cred.login)
    if acc is None:
        return None
    else:
        acc.command_list.append(command_obj)
        update_account(cred.login, acc)
        return CommandInfo(
            command_name=command.command_name,
            participants=command.participants
        )

async def remove_command(cred: AccountRegister, command: CommandInfo):
    command_obj = Command(
        command_name = command.command_name,
        participants = command.participants
    )
    acc = await get_account(cred.login)
    if acc is None:
        return None
    else:
        acc.command_list.remove(command_obj)
        update_account(cred.login, acc)
        return CommandInfo(
            command_name=command.command_name,
            participants=command.participants
        )
            