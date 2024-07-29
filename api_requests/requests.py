from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict, Set, Any, Union, Optional
from dataclasses import dataclass, asdict
from fastapi.encoders import jsonable_encoder

# Elevenlabs request body example
# {
#     "text": "안녕하세요",
#     "model_id": "eleven_turbo_v2_5",
#     "language_code": null,
#     "voice_settings": {
#         "stability": 0.5,
#         "similarity_boost": 0.5
#          "style": 123,
#          "use_speaker_boost": true
#     },
#      "pronunciation_dictionary_locators": [
#          {
#              "pronunciation_dictionary_id": "<string>",
#              "version_id": "<string>"
#          }
#      ],
#     "seed": 123
#      "previous_text": "<string>",
#      "next_text": "<string>",
#      "previous_request_ids": ["<string>"],
#      "next_request_ids": ["<string>"]
# }

DEFAULT_MODEL_ID = "AM_TTS_MODEL_001"
DEFAULT_LANG_CD = "kr"
DEFAULT_STABILITY = 0.5
DEFAULT_SIMILARITY_BOOST = 0.5
DEFAULT_SEED = 123
DEFAULT_SPEED = 1.0
DEFAULT_TTS_PARAMS = {
    "stability": 0.5,
    "similarity_boost": 0.5
}


####################################### 텍스트 음성변환 요청 클래스 ######################################
class TTSRequest(BaseModel):
    """텍스트 음성 변환 요청 클래스"""
    text: str = Field(description="음성 변환 대상 텍스트")
    model_id: str = Field(description="사용 모델 ID", default=DEFAULT_MODEL_ID)
    language_code: str = Field(description="사용 언어 코드", default=DEFAULT_LANG_CD)
    voice_settings: dict = Field(description="음성 변환 파라미터", default=DEFAULT_TTS_PARAMS)
    speed: float = Field(description="재생 속도", default=DEFAULT_SPEED)
    seed: int = Field(description="랜덤 시드", default=DEFAULT_SEED)
    