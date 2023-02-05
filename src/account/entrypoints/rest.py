import logging

from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status

from account.domain.dto import request, response
from account.domain import commands
from account.service_layer.messagebus import MessageBus
from account.service_layer.views import Views

router = APIRouter(
    prefix='/accounts',
    tags=['Account'],
    responses={404: {'description': 'Not found'}},
)
LOG = logging.getLogger('LOG')


@router.get('/{account_number}',
            status_code=status.HTTP_200_OK,
            response_model=response.AccountResponse
            )
async def get_account(
        request: request.AccountRequest = Depends(),
        views: Views = Depends(),
):
    account = await views.get_account_by_account_number(
        account_number=request.account_number
    )

    if account is None:
        raise HTTPException(
            status_code=404,
            detail='Account not found',
        )

    return response.AccountResponse(
        result=response.AccountResponseDTO.build(account)
    )


@router.get(
    '/{account_number}/validation',
    status_code=status.HTTP_200_OK,
    response_model=response.AccountResponse
)
async def validate_account(
        request: request.ValidateAccountRequest = Depends(),
        views: Views = Depends(),
):
    result = await views.is_valid_account_for_amount(
        account_number=request.account_number,
        amount=request.amount
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail='Account not found',
        )

    is_valid, account = result

    if is_valid is False:
        raise HTTPException(
            status_code=400,
            detail='Invalid account for amount',
        )

    return response.AccountResponse(
        result=response.AccountResponseDTO.build(account)
    )


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_account(
        command: commands.Opened = Body(),
        bus: MessageBus = Depends(),
):
    await bus.handle(command)
    return 'OK'
