from pydantic import BaseModel, PositiveInt
from typing import List, Union, Optional, Annotated, Literal
from annotated_types import Len

class SequenceUpdate(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    active: Optional[Literal[0, 1]]

class SequenceCreate(BaseModel):
    name: str
    description: str
    active: Literal[0, 1]

class VideoFileUpdate(BaseModel):
    id: int
    sequence_id: Optional[str]
    name: Optional[str]
    filepath: Optional[str]
    spacial: Optional[Annotated[List, Len(min_length=2, max_length=2)]]
    temporal: Optional[int]
    depth: Optional[int]
    quality: Optional[str]
    gamut: Optional[str]
    active: Optional[Literal[0, 1]]

class VideoFileCreate(BaseModel):
    sequence_id: str
    name: str
    filepath: str
    spacial: Annotated[List, Len(min_length=2, max_length=2)]
    temporal: int
    depth: int
    quality: str
    gamut: str
    active: Literal[0, 1]


class TransmissionConditionUpdate(BaseModel):
    id: int
    name: Optional[str]
    lower_bound: Optional[int]
    upper_bound: Optional[int]
    active: Optional[Literal[0, 1]]

class TransmissionConditionCreate(BaseModel):
    name: str
    lower_bound: int
    upper_bound: int
    active: Literal[0, 1]

class CodecCreate(BaseModel):
    version: str
    active: Literal[0, 1]
    name: str

class CodecUpdate(BaseModel):
    id: int
    version: Optional[str]
    active: Optional[Literal[0, 1]]
    name: Optional[str]

class IdDelete(BaseModel):
    id: int

class NameIdCreate(BaseModel):
    name: str
    active: int

class SequenceCreate(BaseModel):
    name: str
    description: str
    active: int

class SequenceCreate(BaseModel):
    name: str
    description: str
    active: int

class SequenceUpdate(BaseModel):
    id: str
    name: Optional[str]
    description: Optional[str]
    active: Optional[int]

class NameIdUpdate(BaseModel):
    id: int
    name: Optional[str]
    active: Optional[int]

class ToggleActiveRequest(BaseModel):
    active: Literal[0, 1]
    id: int

