import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from core.database import Base
import datetime

class File(Base):
    __tablename__ = "files"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)
    content_type = Column(String(100))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    text_content = Column(Text, nullable=True)  # Für RAG
