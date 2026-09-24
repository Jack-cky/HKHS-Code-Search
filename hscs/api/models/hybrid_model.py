import json
from collections import defaultdict

from .dense_model import DenseSearchEngine
from .sparse_model import SparseSearchEngine


class HybridSearchEngine:
    def __init__(self, model_card: str):
        self.sparse = SparseSearchEngine()
        self.dense = DenseSearchEngine(model_card)

    @property
    def catalogue(self) -> dict[str, str]:
        return self.sparse.catalogue

    @property
    def corpora(self) -> list[str]:
        return self.sparse.corpora

    @property
    def metadata(self) -> list[dict]:
        return self.sparse.metadata

    def _fuse(
        self,
        sparse: list[str],
        dense: list[str],
        c: int,
        weights: tuple[float, float],
    ) -> list[str]:
        scores = defaultdict(float)
        for w, ranking in zip(weights, (sparse, dense)):
            for rank, t in enumerate(ranking, start=1):
                scores[t] += w / (c + rank)

        return sorted(scores, key=scores.get, reverse=True)

    def search(
        self,
        query: str,
        tag: str,
        k: int = 10,
        depth: int = 50,
        n_candidates: int = 50,
        c: int = 10,
        weights: tuple[float, float] = (1.0, 2.0),
    ) -> list[str]:
        sparse = self.sparse.search(query, tag, n_candidates, depth)
        dense = self.dense.search(query, tag, n_candidates, depth)

        return self._fuse(sparse, dense, c=c, weights=weights)[:k]

    def load(self, path: str) -> None:
        with open(f"{path}.meta", "r") as f:
            meta = json.load(f)
        self.sparse.load(path, meta)
        self.dense.load(path, meta)
