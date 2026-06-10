from pydantic import BaseModel, PositiveInt
from typing import List, Union, Optional, Annotated
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

class NameIdCreate(BaseModel):
    name: str

class IdDelete(BaseModel):
    id: int

class NameIdPost(BaseModel):
    id: Optional[int] = None
    name: str

class TransmissionConditionPost(BaseModel):
    id: Optional[int] = None
    name: str
    lower_bound: int
    upper_bound: int

class SequencePost(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

class VideoFilePost(BaseModel):
    id: Optional[int] = None
    sequence_id: str
    name: str
    filepath: str
    spacial: Annotated[List, Len(min_length=2, max_length=2)]
    temporal: int
    depth: int
    quality: str
    gamut: str