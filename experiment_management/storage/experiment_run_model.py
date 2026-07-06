from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from storage.db import Base


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    id = Column(Integer, primary_key=True)
    groupId = Column(
        Integer,
        ForeignKey("experiment_groups.id")
    )
    sequenceCode = Column(String)
    encoderData = Column(JSONB)
    sequenceData = Column(JSONB)
    networkData = Column(JSONB)
    status = Column(String)
    createdAt = Column(DateTime)