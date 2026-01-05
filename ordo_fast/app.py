from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from ordo_fast.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'olá mundo'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_html():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <p>Olá Mundo!</p>
      </body>
    </html>"""
