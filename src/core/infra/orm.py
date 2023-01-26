from account.adapters.orm import account_mapper


async def start_mappers(engine):
    mappers = [account_mapper]
    for mapper in mappers:
        await mapper(engine)
