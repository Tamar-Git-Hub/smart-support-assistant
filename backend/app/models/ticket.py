from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    subject = Column(String(500), nullable=False)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    priority_level = Column(Integer, default=1)
    status = Column(String(50), default="open")  
    sentiment_score = Column(Float)
    urgency_score = Column(Float)
    customer_email = Column(String(255))
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP, server_default=text("NOW()"))
    resolved_at = Column(TIMESTAMP)
    source_channel = Column(String(100))
    embedding_vector = Column(String) 
