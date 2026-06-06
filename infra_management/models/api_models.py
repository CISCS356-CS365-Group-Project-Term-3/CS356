from pydantic import BaseModel, PositiveInt
from typing import List, Union

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

class CreateProjectType(BaseModel):
    name: str

class DeleteProjectType(BaseModel):
    id: int

class UpdateProjectType(BaseModel):
    id: int
    name: str

class PostProjectType(BaseModel):
    root: Union[UpdateProjectType, CreateProjectType]
