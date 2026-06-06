from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from storage.db import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    project_type_id = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False)

    data = Column(JSONB, nullable=False)