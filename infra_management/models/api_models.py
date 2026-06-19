from pydantic import BaseModel, PositiveInt
from typing import List, Union, Optional, Annotated, Literal
from annotated_types import Len

# class ProjectType(BaseModel):
#     id: int
#     name: str

# class EncoderType(BaseModel):
#     id: int
#     name: str

# class Codec(BaseModel):
#     id: int
#     name: str

# class EncoderMode(BaseModel):
#     id: int
#     name: str

# class VideoFile(BaseModel):
#     id: int
#     name: str
#     spacial: List[PositiveInt]
#     temporal: PositiveInt
#     depth: PositiveInt
#     filepath: str
#     quality: str
#     gamut: str

# class Sequences(BaseModel):
#     id: int
#     name: str
#     description: str
#     video_files: List[VideoFile]

# class Topology(BaseModel):
#     id: int
#     name: str

# class TransmissionCondition(BaseModel):
#     id: int
#     name: str
#     lower_bound: str
#     upper_bound: str

# class UiOptions(BaseModel):
#     project_types: List[ProjectType]
#     encoder_type: List[EncoderType]
#     codecs: List[Codec]
#     encoder_modes: List[EncoderMode]
#     sequences: List[VideoFile]

class ToggleActiveRequest(BaseModel):
    active: Literal[0, 1]
    id: int