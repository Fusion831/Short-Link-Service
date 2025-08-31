from pydantic import BaseModel

class UrlCreate(BaseModel):
    long_url: str


class UrlInfo(UrlCreate):
    short_link:str
    class Config:
        from_attributes = True
    