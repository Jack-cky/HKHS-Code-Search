import json
from collections import defaultdict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class DenseSearchEngine:
    def __init__(self, model_card: str):
        self.model = SentenceTransformer(
            model_card,
            backend="onnx",
            model_kwargs={"provider": "CPUExecutionProvider"},
        )
        self.vector_index = faiss.IndexFlatIP(
            self.model.get_embedding_dimension()
        )
        self.catalogue = {}
        self.corpora = []
        self.metadata = []

    def _search_docs(
        self,
        query: str,
        depth: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        vectors = (
            self.model.encode(query, convert_to_numpy=True)
            .reshape(1, -1)
        )
        faiss.normalize_L2(vectors)
        scores, indices = self.vector_index.search(vectors, depth)

        return scores[0], indices[0]

    def _score(self, scores: list[float], pool: int, decay: float) -> float:
        top_scores = sorted(scores, reverse=True)[:pool]

        return sum(score * decay**i for i, score in enumerate(top_scores))

    def search(
        self,
        query: str,
        tag: str,
        k: int = 10,
        depth: int = 100,
        pool: int = 4,
        decay: float = 0.5,
    ) -> list[str]:
        scores, indices = self._search_docs(query, depth)
        mask = indices != -1
        floor = min(scores[mask], default=0.0)

        grouped = defaultdict(list)
        for s, idx in zip(scores[mask], indices[mask]):
            grouped[self.metadata[idx][tag]].append(s - floor)

        predictions = sorted(
            grouped,
            key=lambda x: self._score(grouped[x], pool, decay),
            reverse=True,
        )[:k]

        return predictions

    def load(self, path: str) -> None:
        self.vector_index = faiss.read_index(f"{path}.faiss")

        with open(f"{path}.meta", "r") as f:
            meta = json.load(f)
            self.catalogue = meta["catalogue"]
            self.corpora = meta["corpora"]
            self.metadata = meta["metadata"]
