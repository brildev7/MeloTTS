from datetime import datetime
from enum import Enum
from copy import deepcopy
from typing import List, Dict, Set, Any, Union, Annotated, Optional
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from routers.base import Tags
from util.logger import logger


PREFIX_URL = "/v1"
router = APIRouter(
    prefix=PREFIX_URL,
    tags=[Tags.tool],
    responses={404: {"description": "Not found"},
               200: {"description": "OK"},
               400: {"description": "Bad Request"},
               422: {"description": "Unprocessible Entity"},
               500: {"description": "Internal Error"}},
)

@router.get("/session", 
            status_code=status.HTTP_200_OK,
            summary="Health check",
            description="",
            include_in_schema=True,
            tags=[Tags.tool],)
async def session():
    logger.info("/session")
    return {"status":"ok"}