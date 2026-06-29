from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from storage.db import Base

class ExperimentGroup(Base):
    __tablename__ = "experiment_groups"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    name = Column(String)
    status = Column(String)
    projectTypeId = Column(Integer)
    createdAt = Column(DateTime)
    draftData = Column(JSONB)