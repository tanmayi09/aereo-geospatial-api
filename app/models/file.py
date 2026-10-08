from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    crs = Column(String, nullable=True)
    feature_count = Column(Integer, nullable=False)
    features = Column(Text, nullable=False)
    measurements = Column(Text, nullable=False)