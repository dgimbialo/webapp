from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .meta import Base

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    publication_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user_name = Column(Text, nullable=False)
    user = relationship('User', backref='comments')
    page_id = Column(ForeignKey('pages.id'), nullable=False)
