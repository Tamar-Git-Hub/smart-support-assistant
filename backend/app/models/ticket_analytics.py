from sqlalchemy import Column, Integer, Float, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class TicketAnalytics(Base):
    __tablename__ = "ticket_analytics"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"))
    response_time_minutes = Column(Integer)
    resolution_time_hours = Column(Integer)
    agent_satisfaction_score = Column(Integer)
    customer_satisfaction_score = Column(Integer)
    escalation_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
