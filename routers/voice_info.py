from datetime import datetime
from enum import Enum
from copy import deepcopy
from typing import List, Dict, Set, Any, Union, Annotated, Optional
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from routers.base import Tags
from config.config import voices
from util.logger import logger


PREFIX_URL = "/v1"
router = APIRouter(
    prefix=PREFIX_URL,
    tags=[Tags.info],
    responses={404: {"description": "Not found"},
               200: {"description": "OK"},
               400: {"description": "Bad Request"},
               422: {"description": "Unprocessible Entity"},
               500: {"description": "Internal Error"}},
)

@router.get("/voice", 
            status_code=status.HTTP_200_OK,
            summary="Get voice list",
            description="Get voice list",
            include_in_schema=True,
            tags=[Tags.info],)
async def voice():
    logger.info("/voice")
    return {"voices":voices}