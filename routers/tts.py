import os
import random
from datetime import datetime
from enum import Enum
from copy import deepcopy
from typing import List, Dict, Set, Any, Union, Annotated, Optional
import hashlib
import uuid
import shutil
# from redis import Redis
from httpx import HTTPError
# cache_contents = Redis(
#     host=cache_config.cache_host, 
#     port=cache_config.cache_port,
#     db=0,
#     username=None if run_level == "dev" else cache_config.cache_id,
#     password=cache_config.cache_pass)

import httpx
from fastapi import status
from fastapi import Body, Query
from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from routers.base import Tags
from api_requests.requests import TTSRequest
from api_requests.requests import (
    DEFAULT_MODEL_ID,
    DEFAULT_LANG_CD,
    DEFAULT_SEED,
    DEFAULT_SPEED
)
from melo.api import TTS
from util.logger import logger
OUTPUT_DIR = "/data/aibox_tts/data/"


################################### MODEL INITIALIZE ###################################
# CUDA_DEVICES = ["cuda:0", "cuda:1"]
CUDA_DEVICES = ["cuda:0"]
tts_ko_models = [
    TTS(language='KR', device=device) for device in CUDA_DEVICES
]
logger.info("=================== tts korean models ===================")
for model in tts_ko_models:
    logger.info("init model device: {}".format(model.device))


###################################### API ROUTER ######################################
PREFIX_URL = "/v1"
router = APIRouter(
    prefix=PREFIX_URL,
    tags=[Tags.tts],
    responses={404: {"description": "Not found"},
               201: {"description": "Created"},
               400: {"description": "Bad Request"},
               422: {"description": "Unprocessible Entity"},
               500: {"description": "Internal Error"}},
)


#################################### HELPER METHODS ####################################
# def _set_cache(content: ContentsBase, hash: str, text: str):
#     cache_contents.set(hash, text)
# Speed is adjustable

def _make_output_dir():
    today = datetime.now().strftime("%Y%m%d")
    OUTPUT_PATH = OUTPUT_DIR + today
    if not os.path.isdir(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    return OUTPUT_PATH + "/"

def _generate(model: TTS, text: str, lang_cd: str = DEFAULT_LANG_CD, speed: int = DEFAULT_SPEED):
    try:
        speaker_ids = model.hps.data.spk2id
        
        random_id = str(uuid.uuid4())
        filename = "audio_file_id_" + random_id + ".wav"
        outdir = _make_output_dir()
        output_filepath = outdir + filename        
        model.tts_to_file(text, speaker_ids[lang_cd.upper()], output_filepath, speed=speed)
    except Exception as e:
        logger.error(e)
        return None, None
    return output_filepath, filename
    

#################################### API ENDPOINTS ####################################
@router.post("/text-to-speech", 
             status_code=status.HTTP_201_CREATED,
             summary="Text to Speech",
             description="Text to Speech",
             include_in_schema=True,
             tags=[Tags.tts],)
async def generate(
    request: Annotated[
        TTSRequest,
        Body(
            examples=[
                {
                    "text": "안녕하세요",
                    "model_id": DEFAULT_MODEL_ID,
                    "language_code": DEFAULT_LANG_CD,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                        # "style": 123,
                        # "use_speaker_boost": True
                    },
                    "speed": DEFAULT_SPEED
                }
            ],
        ),
    ]
):
    logger.info("/text-to-speech")
    json_req = request.model_dump()
    
    text = json_req.get("text", None)
    # model_id = json_req.get("model_id", None)
    lang_cd = json_req.get("language_code", None)
    # voice_settings = json_req.get("voice_settings", None)
    speed = json_req.get("speed", None)
        
    # check translation contents and languages
    if not all([text, lang_cd, speed]):
        raise RequestValidationError("Text or source language code or speed not provided.")
    
    try:
        model = random.choice(tts_ko_models)
        logger.debug(f"using device: {model.device}")
        
        output_file, filename = _generate(model, text, lang_cd=lang_cd, speed=speed)
        if not output_file or not filename:
            raise RuntimeError("generate wave file failed.")
        
        logger.info("/text-to-speech complete")
        res = FileResponse(path=output_file, 
                          media_type="audio/wav", 
                          status_code=status.HTTP_201_CREATED, 
                          filename=filename)
    except Exception as e:
        logger.error(e)
        res = FileResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        del model
    return res
    