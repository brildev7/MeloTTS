import os
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pydantic import field_validator
from pydantic_settings import BaseSettings
from util.logger import logger
    
###################################### RUN LEVEL #######################################
TTS_API_RUN_LEVEL = os.getenv("TTS_API_RUN_LEVEL")
TTS_API_RUN_LEVEL = "DEV" if not TTS_API_RUN_LEVEL else TTS_API_RUN_LEVEL
run_level = TTS_API_RUN_LEVEL.lower()


##################################### VOICE INFO #######################################
voice_list = List[Dict[str, Any]]

CONFIG_PATH = "./config/voices.yaml"
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)
    voice_list = config['voices']


@dataclass
class Voice:
    id: str
    name: Optional[str]
    model_id: str
    model_desc: Optional[str]
    language: str
    gender: str
    type: Optional[str]
    dataset: Optional[str]
    dataset_detail: Optional[str]
    train_info: Optional[Dict]
    
voices = [Voice(**voice['voice']) for voice in voice_list]
model_voice_dict = dict()
for voice in voices:
    if voice.model_id not in model_voice_dict.keys():
        model_voice_dict[voice.model_id] = [voice.id]
    else:
        model_voice_dict[voice.model_id].append(voice.id)
        
logger.info("=============== provided voices ============")
logger.info(voices)

logger.info("============== model-voice dict ============")
logger.info(model_voice_dict)
