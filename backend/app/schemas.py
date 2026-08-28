from typing import Literal
from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str
    provider: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    mode: Literal["ai", "retrieval-only"]


class PropertyRecord(BaseModel):
    provider: str
    title: str
    location: str = ""
    property_type: str = ""
    price: str = ""
    bedrooms: str = ""
    bathrooms: str = ""
    description: str = ""
    url: str
