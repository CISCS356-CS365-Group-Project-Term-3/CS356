from pydantic import BaseModel, PositiveInt
from typing import List, Union, Optional, Annotated, Literal
from annotated_types import Len

class SequenceUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[Literal[0, 1]] = None

class SequenceCreate(BaseModel):
    name: str
    description: str

class VideoFileUpdate(BaseModel):
    id: int
    sequence_id: Optional[str] = None
    name: Optional[str] = None
    filepath: Optional[str] = None
    spacial: Optional[Annotated[List, Len(min_length=2, max_length=2)]] = None
    temporal: Optional[int] = None
    depth: Optional[int] = None
    quality: Optional[str] = None
    gamut: Optional[str] = None
    active: Optional[Literal[0, 1]] = None

class VideoFileCreate(BaseModel):
    sequence_id: str
    name: str
    filepath: str
    spacial: Annotated[List, Len(min_length=2, max_length=2)]
    temporal: int
    depth: int
    quality: str
    gamut: str


class TransmissionConditionUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None
    unit: Optional[str] = None
    active: Optional[Literal[0, 1]] = None

class TransmissionConditionCreate(BaseModel):
    name: str
    lower_bound: int
    upper_bound: int
    unit: str

class CodecCreate(BaseModel):
    version: str
    name: str
    encoder_type_id: int

class CodecUpdate(BaseModel):
    id: int
    version: Optional[str] = None
    active: Optional[Literal[0, 1]] = None
    name: Optional[str] = None
    encoder_type_id: Optional[int] = None

class IdDelete(BaseModel):
    id: int

class NameIdCreate(BaseModel):
    name: str

class NameIdUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    active: Optional[Literal[0, 1]] = None

class EncoderTypeCreate(BaseModel):
    name: str
    description: str

class EncoderTypeUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[Literal[0, 1]] = None
