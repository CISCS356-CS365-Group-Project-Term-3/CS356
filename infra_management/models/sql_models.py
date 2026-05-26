from __future__ import annotations

from sqlalchemy import Integer, String, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from util.engine import Base
from typing import List

class ProjectType(Base):
    __tablename__ = "PROJECT_TYPE"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class EncoderType(Base):
    __tablename__ = "ENCODER_TYPE"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class Codec(Base):
    __tablename__ = "CODEC"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class EncoderModes(Base):
    __tablename__ = "ENCODER_MODES"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class Quality(Base):
    __tablename__ = "QUALITY"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class Gamut(Base):
    __tablename__ = "GAMUT"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class Topology(Base):
    __tablename__ = "TOPOLOGY"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))

class TransmissionCondition(Base):
    __tablename__ = "TRANSMISSION_CONDITION"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    lower_bound = mapped_column(Integer)
    upper_bound = mapped_column(Integer)

class FrameRate(Base):
    __tablename__ = "FRAME_RATE"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    frame_rate = mapped_column(Integer)


class Depth(Base):
    __tablename__ = "DEPTH"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    depth = mapped_column(Integer)

class Resolution(Base):
    __tablename__ = "RESOLUTION"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    x = mapped_column(Integer)
    y = mapped_column(Integer)

video_file_resolution = Table(
    "VIDEO_FILE_RESOLUTION",
    Base.metadata,
    Column("video_id", ForeignKey("VIDEO_FILE.id"), primary_key=True),
    Column("resolution_id", ForeignKey("RESOLUTION.id"), primary_key=True),
)

video_file_frame_rate = Table(
    "VIDEO_FILE_FRAME_RATE",
    Base.metadata,
    Column("video_id", ForeignKey("VIDEO_FILE.id"), primary_key=True),
    Column("frame_rate_id", ForeignKey("FRAME_RATE.id"), primary_key=True),
)

video_file_depth = Table(
    "VIDEO_FILE_DEPTH",
    Base.metadata,
    Column("video_id", ForeignKey("VIDEO_FILE.id"), primary_key=True),
    Column("depth_id", ForeignKey("DEPTH.id"), primary_key=True),
)

class VideoFile(Base):
    __tablename__ = "VIDEO_FILE"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    filepath = mapped_column(String(255))
    resolutions: Mapped[List[Resolution]] = relationship(secondary=video_file_resolution)
    framerates: Mapped[List[FrameRate]] = relationship(secondary=video_file_frame_rate)
    depths: Mapped[List[Depth]] = relationship(secondary=video_file_depth)


# class VideoFileResolution(Base):
#     video_id = mapped_column(Integer)
#     resolution_id = mapped_column(Integer)

# class VideoFileFrameRate(Base):
#     video_id = mapped_column(Integer)
#     frame_rate_id = mapped_column(Integer)

# class VideoFileDepth(Base):
#     video_id = mapped_column(Integer)
#     depth_id = mapped_column(Integer)
