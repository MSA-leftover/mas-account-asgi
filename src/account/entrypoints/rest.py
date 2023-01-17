import logging

from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/accounts",
    tags=["Loadbalancer"],
    responses={404: {"description": "Not found"}},
)
LOG = logging.getLogger("LOG")


@router.get("/", status_code=status.HTTP_200_OK)
async def heath_check():
    return {"message": "healthy"}
