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

DEFAULT_MODEL_ID = "6c8d49f3-50b4-4025-bf5b-16e813a2686d" # melo tts pretrained korean model
DEFAULT_VOICE_ID = "b540ea02-6c7a-478e-9e60-5d766118f84a" # melo tts default korean voice
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
    voice_id: str = Field(description="사용 음성 ID", default=DEFAULT_VOICE_ID)
    model_id: str = Field(description="사용 모델 ID", default=DEFAULT_MODEL_ID)
    language_code: str = Field(description="사용 언어 코드", default=DEFAULT_LANG_CD)
    voice_settings: dict = Field(description="음성 변환 파라미터", default=DEFAULT_TTS_PARAMS)
    speed: float = Field(description="재생 속도", default=DEFAULT_SPEED)
    seed: int = Field(description="랜덤 시드", default=DEFAULT_SEED)
    