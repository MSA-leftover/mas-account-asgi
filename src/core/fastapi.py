from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from account.entrypoints.rest import router as account_router
from core.orm import start_mappers

app = FastAPI()
app.include_router(account_router)


@app.on_event("startup")
def startup_event():
    start_mappers()


@app.on_event("shutdown")
def shutdown_event():
    clear_mappers()
