from typing import Literal

from pydantic import BaseModel

Level = Literal["chapter", "heading", "subheading", "hkhs"]


class SearchResult(BaseModel):
    code: str
    hierarchy: list[str]


class SearchResponse(BaseModel):
    query: str
    level: Level
    results: list[SearchResult]
