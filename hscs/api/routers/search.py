from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..schemas import Level, SearchResponse, SearchResult
from ..services import SearchEngine, get_engine

router = APIRouter(tags=["search"])


def profile_hierarchy(code: str, catalogue: dict[str, str]) -> list[str]:
    return [
        catalogue[code[: i + 2]]
        for i in range(0, len(code), 2)
        if code[: i + 2] in catalogue
    ]


@router.get("/search", response_model=SearchResponse)
def search(
    engine: Annotated[SearchEngine, Depends(get_engine)],
    q: Annotated[str, Query(min_length=1, max_length=50)],
    level: Level,
    k: Annotated[int, Query(ge=1, le=30)] = 10,
):
    results = [
        SearchResult(
            code=code,
            hierarchy=profile_hierarchy(code, engine.catalogue),
        )
        for code in engine.search(q, level, k)
    ]
    return SearchResponse(query=q, level=level, results=results)
