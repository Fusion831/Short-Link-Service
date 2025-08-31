from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

# This is the base class our model will inherit from
Base = declarative_base()

class URL(Base):
    # This is the actual table name that will be created in the database
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)

    # This ensures the 'short_code' column must be unique at the database level.
    
    __table_args__ = (UniqueConstraint('short_code', name='uq_short_code'),)
    