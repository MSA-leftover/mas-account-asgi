from random import randrange

from account.domain import events, commands, exceptions, entity
from account.service_layer import uow


def generate_account_number() -> str:
    return ''.join(map(str, [randrange(10) for _ in range(15)]))


async def open_account(
        cmd: commands.Opened,
        uow: uow.AbstractUnitOfWork,
):
    async with uow:
        account = True
        while account:
            new_account_number = generate_account_number()
            account = await uow.repository.get(new_account_number)

        account = entity.Account(
            account_number=new_account_number,
            name=cmd.name,
            user_id=cmd.user_id,
            cash=cmd.cash,
            events=[]
        )

        uow.repository.add(account)
        await uow.commit()

        return account


async def withdraw(
        cmd: commands.Withdraw,
        uow: uow.AbstractUnitOfWork,
):
    async with uow:
        account = await uow.repository.get(account_number=cmd.account_number)
        if account is None:
            raise exceptions.InvalidAccount

        account.withdraw(amount=cmd.amount)
        await uow.commit()


async def deposit(
        cmd: commands.Deposit,
        uow: uow.AbstractUnitOfWork,
):
    async with uow:
        account = await uow.repository.get(account_number=cmd.account_number)
        if account is None:
            raise exceptions.InvalidAccount

        account.deposit(amount=cmd.amount)
        await uow.commit()


async def insufficient_cash_from_account(
        event: events.InsufficientCash,
        uow: uow.AbstractUnitOfWork,
):
    pass


def EVENT_HANDLERS():
    return {
        events.InsufficientCash: [insufficient_cash_from_account],
        events.Deposited: [],
        events.Withdrew: [],
    }


def COMMAND_HANDLERS():
    return {
        commands.Deposit: deposit,
        commands.Withdraw: withdraw,
        commands.Opened: open_account,
    }
