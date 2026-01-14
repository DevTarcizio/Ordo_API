from http import HTTPStatus

from fastapi import FastAPI

from ordo_fast.database import close_engine
from ordo_fast.routers import auth, task, users
from ordo_fast.schemas import Message

app = FastAPI(title='Ordo Praesidium')
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(task.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'olá mundo'}


# Adicionado para evitar travamentos do terminal
@app.on_event('shutdown')
async def shutdown_event():
    await close_engine()
