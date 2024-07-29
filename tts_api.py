import os
from datetime import datetime, time, timedelta, timezone
from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import Union, Annotated, List, Dict
from typing_extensions import Annotated as ExtAnnotated
import logging

from fastapi import FastAPI, Query, Path, Body, Cookie, Form, status, Header
from fastapi import Request, Response
from fastapi import File, UploadFile
from fastapi import HTTPException
from fastapi import Depends
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import fire

from routers.health_check import router as health_check_router
from routers.tts import router as tts_router
from routers.base import Tags
from util.logger import get_logger, PROJECT_NAME, logger

app = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = datetime.now() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

################################## exception handlers ##################################
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

##################################### add routers ######################################
app.include_router(tts_router)
app.include_router(health_check_router)

################################ entry point function ##################################
def start(
    host: str = "0.0.0.0",
    port: int = 15300,
    reload: bool = False,
    workers: int = 2,
    log_level: str = "debug",
    limit_concurrency: int = 100,
):
    uvicorn.run(
        "tts_api:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level,
        limit_concurrency=limit_concurrency,
    )

if __name__ == "__main__":
    fire.Fire(start)
