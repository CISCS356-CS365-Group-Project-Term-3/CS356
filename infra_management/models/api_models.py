from pydantic import BaseModel
from typing import List

class ProjectType(BaseModel):
    id: int
    name: str

class EncoderType(BaseModel):
    id: int
    name: str
    active_codecs: List[int]

class Codec(BaseModel):
    id: int
    name: str

class EncoderMode(BaseModel):
    id: int
    name: str

class VideoFile(BaseModel):
    id: int
    name: str
    available_spatials: List[int]
    available_temporals: List[int]
    available_depths: List[int]

class Resolution(BaseModel):
    id: int
    name: str
    value: str

class FrameRate(BaseModel):
    id: int
    name: str
    value: str

class Quality(BaseModel):
    id: int
    name: str

class Depth(BaseModel):
    id: int
    name: str

class Gamut(BaseModel):
    id: int
    name: str

class Topology(BaseModel):
    id: int
    name: str

class TransmissionCondition(BaseModel):
    id: int
    name: str
    lower_bound: str
    upper_bound: str

class UiOptions(BaseModel):
    project_types: List[ProjectType]
    encoder_type: List[EncoderType]
    codecs: List[Codec]

