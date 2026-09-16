import json
import pickle
import re
from collections import defaultdict

import numpy as np
from nltk.stem import WordNetLemmatizer


class SparseSearchEngine:
    def __init__(self):
        self.model = None
        self.catalogue = {}
        self.corpora = []
        self.metadata = []
        self.lemmatiser = WordNetLemmatizer()

    def _clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _lemmatise_desc(self, text: str) -> str:
        return " ".join(
            self.lemmatiser.lemmatize(word)
            for word in self._clean_text(text).split()
        )

    def _tokenise(self, text: str) -> list[str]:
        return re.findall(r"\w+", text.lower())

    def _search_docs(self, query: str) -> np.ndarray:
        tokens = self._tokenise(self._lemmatise_desc(query))

        return self.model.get_scores(tokens)

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
        scores = self._search_docs(query)
        d = min(depth, len(scores))
        top = np.argpartition(-scores, d - 1)[:d]
        top = np.sort(top)[np.argsort(-scores[np.sort(top)], kind="stable")]

        grouped = defaultdict(list)
        for i in top:
            if scores[i] > 0:
                grouped[self.metadata[i][tag]].append(scores[i])

        predictions = sorted(
            grouped,
            key=lambda t: self._score(grouped[t], pool, decay),
            reverse=True,
        )[:k]

        return predictions

    def load(self, path: str) -> None:
        with open(f"{path}.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open(f"{path}.meta", "r") as f:
            meta = json.load(f)
            self.catalogue = meta["catalogue"]
            self.corpora = meta["corpora"]
            self.metadata = meta["metadata"]
