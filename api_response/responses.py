from pydantic import BaseModel, Field
from typing import List, Dict, Set, Any, Union
from dataclasses import dataclass, asdict
from fastapi.responses import FileResponse


####################################### 텍스트 음성변환 응답 클래스 ######################################
class TTSResponse(FileResponse):
    pass
