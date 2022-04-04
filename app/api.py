from fastapi import FastAPI, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from typing import List
from loguru import logger


app = FastAPI()

list_of_usernames = list()
templates = Jinja2Templates(directory="app/templates")


origins = [
    "http://localhost:8080",
    "localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"title":"Test"}


@app.get("/dash_way")
async def dash_way():
    return {"title":"Test"}

