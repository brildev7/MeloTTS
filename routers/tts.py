import os
import random
from datetime import datetime
from enum import Enum
from copy import deepcopy
from typing import List, Dict, Set, Any, Union, Annotated, Optional
import hashlib
import uuid
import shutil
import json
from json import JSONEncoder
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
from fastapi.responses import FileResponse, Response, JSONResponse
from routers.base import Tags
from api_requests.requests import TTSRequest
from api_requests.requests import (
    DEFAULT_VOICE_ID,
    DEFAULT_MODEL_ID,
    DEFAULT_LANG_CD,
    DEFAULT_SEED,
    DEFAULT_SPEED,
    DEFAULT_NOISE_SCALE,
    DEFAULT_NOISE_SCALE_W,
    DEFAULT_SDP_RATIO,
    DEFAULT_SIMILARITY_BOOST,
    DEFAULT_STABILITY,
    DEFAULT_TTS_PARAMS
)
from melo.api import TTS
from config.config import voices
voice_ids = [voice.id for voice in voices]
from config.config import model_voice_dict
from config.config import Voice

from util.logger import logger
OUTPUT_DIR = "/data/aibox_tts/data/"
OUTPUT_DIR_TMP = "/data/aibox_tts/data/tmp"
BASE_DIR = "/ssd_data/code/aibox_tts"
MODEL_DIR = "/ssd_data/code/aibox_tts/models"

################################### MODEL INITIALIZE ###################################
CUDA_DEVICES = ["cuda:0", "cuda:1"]
def _get_model_info(voice: Voice):
    def _get_model_path(model_id: str, voice_id: str):
        return os.path.join(MODEL_DIR, model_id, voice_id)
        
    language = voice.language
    device = CUDA_DEVICES[0]
    use_hf = False
    config_path = _get_model_path(voice.model_id, voice.id) + f"/config.json"
    logger.info(f"config path: {config_path}")
    
    ckpt_path = _get_model_path(voice.model_id, voice.id) + f"/G.pth"
    logger.info(f"ckpt path: {ckpt_path}")
    
    return {
        "language": language.upper(),
        "device": device,
        "use_hf": use_hf,
        "config_path": config_path,
        "ckpt_path": ckpt_path
    }

# load models
tts_models = list()
for voice in voices[:1]:
    model_info = _get_model_info(voice)
    # tts_models.append(TTS(**model_info))
    tts_models.append(TTS(language=model_info['language'],
                          config_path=model_info['config_path'],
                          ckpt_path=model_info['ckpt_path']))
    
logger.info(f"tts voice count: {len(tts_models)}")
logger.info("=================== loaded tts models ===================")
for model in tts_models:
    logger.info(model)
    
################################## Text to Speech Test #################################
try:
    tts_models[0].tts_to_file(
    text="만나서 반가워요.", 
    speaker_id=0, 
    output_path=OUTPUT_DIR_TMP + "/tmp.wav", 
    sdp_ratio=DEFAULT_SDP_RATIO,
    noise_scale=DEFAULT_NOISE_SCALE,
    noise_scale_w=DEFAULT_NOISE_SCALE_W,
    speed=DEFAULT_SPEED)
except Exception as e:
    logger.error(e)


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
        logger.debug(f"speaker ids: {speaker_ids}")
        
        random_id = str(uuid.uuid4())
        filename = "audio_file_id_" + random_id + ".wav"
        outdir = _make_output_dir()
        output_filepath = outdir + filename        
        model.tts_to_file(
            text=text, 
            speaker_id=speaker_ids[lang_cd.upper()], 
            output_path=output_filepath, 
            sdp_ratio=DEFAULT_SDP_RATIO,
            noise_scale=DEFAULT_NOISE_SCALE,
            noise_scale_w=DEFAULT_NOISE_SCALE_W,
            speed=speed)
    except Exception as e:
        logger.error(f"error: {e}")
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
                    "voice_id": DEFAULT_VOICE_ID,
                    "model_id": DEFAULT_MODEL_ID,
                    "language": DEFAULT_LANG_CD,
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
    
    model_id = json_req.get("model_id")
    voice_id = json_req.get("voice_id")
    text = json_req.get("text", None)
    lang_cd = json_req.get("language", None)
    # voice_settings = json_req.get("voice_settings", None)
    speed = json_req.get("speed", None)
    logger.debug(f"model id: {model_id}")
    logger.debug(f"voice id: {voice_id}")
    logger.debug(f"text: {text}")
    logger.debug(f"language code: {lang_cd}")
    
    if model_id not in model_voice_dict.keys():
        raise RequestValidationError("model id not found")
    
    voice_ids = model_voice_dict[model_id]
    if not voice_ids or len(voice_ids) < 1:
        raise RequestValidationError("voice id not found")
    
    # check translation contents and languages
    if not all([text, lang_cd, speed]):
        raise RequestValidationError("Text or source language code or speed not provided.")
    
    try:
        #TODO: get model by filter id
        model = tts_models[0]
        logger.info(f"model's hyperparameter: {model.hps}")
        logger.debug(f"using device: {model.device}")
        
        output_file, filename = _generate(model, text, lang_cd=lang_cd.upper(), speed=speed)
        if not output_file or not filename:
            raise RuntimeError("generate wave file failed.")
        
        logger.info("/text-to-speech complete")
        res = FileResponse(path=output_file, 
                          media_type="audio/wav", 
                          status_code=status.HTTP_201_CREATED, 
                          filename=filename)
    except Exception as e:
        logger.error(e)
        content = {
            "error_code": "5000",
            "error_message": f"{e}",
            "error_descripton": "텍스트 음성 변환에 실패했습니다."
        }
        # content = jsonable_encoder(content)
        res = JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        del model
    return res
    