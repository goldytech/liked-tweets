from pydantic import BaseModel, HttpUrl
from typing import Optional


class Tweet(BaseModel):
    id: str
    text: str
    url: str
    username: str
    media_url: Optional[str] = ""
