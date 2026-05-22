from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class PostUpdate(BaseModel):
    caption: Optional[str] = Field(default=None, max_length=2200)


class PostRead(BaseModel):
    id: int
    caption: str
    image_url: str
    image_file_id: Optional[str] = None
    created_at: datetime
