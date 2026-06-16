from __future__ import annotations

from sqlalchemy import Integer, String, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from util.engine import Base
from typing import List

class ProjectType(Base):
    __tablename__ = "project_type"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class EncoderType(Base):
    __tablename__ = "encoder_type"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    description = mapped_column(String(255))

class Codec(Base):
    __tablename__ = "codec"
    id = mapped_column(Integer, primary_key=True)
    version = mapped_column(String(64))
    active = mapped_column(Integer)
    encoder_type = mapped_column(Integer, ForeignKey("encoder_type.id"))
    name = mapped_column(String(255))

class EncoderMode(Base):
    __tablename__ = "encoder_modes"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class Topology(Base):
    __tablename__ = "topology"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class TransmissionCondition(Base):
    __tablename__ = "transmission_conditions"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    lower_bound = mapped_column(Integer)
    upper_bound = mapped_column(Integer)

class Sequence(Base):
    __tablename__ = "sequence"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(64))
    description = mapped_column(String(255))

class VideoFile(Base):
    __tablename__ = "video_file"
    id = mapped_column(Integer, primary_key=True)
    sequence_id = mapped_column(ForeignKey("sequence.id"))
    name = mapped_column(String(255))
    filepath = mapped_column(String(255))
    spacial_x = mapped_column(Integer)
    spacial_y = mapped_column(Integer)
    temporal = mapped_column(Integer)
    depth = mapped_column(Integer)
    quality = mapped_column(String(64))
    gamut = mapped_column(String(64))