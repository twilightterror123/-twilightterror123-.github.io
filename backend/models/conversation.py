import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from core.database import Base
import datetime

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="Neues Gespräch")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
