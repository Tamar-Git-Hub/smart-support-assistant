from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    auto_response_template = Column(String)
    sla_hours = Column(Integer, default=24)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP, server_default=text("NOW()"))
