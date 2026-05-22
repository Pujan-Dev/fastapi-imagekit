from sqlalchemy import Column, DateTime, Integer, String, Text, func

from database.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(Text, nullable=False, default="")
    image_url = Column(String, nullable=False)
    image_file_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)