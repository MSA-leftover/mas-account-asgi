from account.adapters.orm import account_mapper


def start_mappers():
    mappers = [account_mapper]
    for mapper in mappers:
        mapper()
