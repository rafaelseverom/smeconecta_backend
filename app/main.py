from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from http import HTTPStatus

import jwt
from datetime import datetime, timedelta


##
from app.routers.teacherRoutes import router as teacher_router

#
from app.schemas.user import *
from app.schemas.teacherResponse import *


# uvicorn app.main:app --reload
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite qualquer origem (qualquer site)
    allow_methods=["*"],  # permite todos os métodos HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # permite todos os header
)

app.include_router(teacher_router)

