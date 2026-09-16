from functools import lru_cache
from pathlib import Path

import nltk
from huggingface_hub import snapshot_download

from .config import BASE_DIR, settings


def download_model_artefacts() -> None:
    index, model = Path(settings.search_index), Path(settings.search_model)
    patterns = []
    if not index.with_suffix(".meta").exists():
        patterns.append(f"{index.relative_to(BASE_DIR)}.*")
    if settings.search_engine != "sparse" and not model.is_dir():
        patterns.append(f"{model.relative_to(BASE_DIR)}/**")
    if patterns:
        snapshot_download(
            repo_id=settings.search_repo,
            local_dir=BASE_DIR,
            allow_patterns=patterns,
        )
    if settings.search_engine != "dense":
        nltk.data.path.append(settings.nltk_data)

        try:
            nltk.data.find("corpora/wordnet")
        except LookupError:
            nltk.download(
                "wordnet",
                download_dir=settings.nltk_data,
                quiet=True,
            )


@lru_cache(maxsize=1)
def get_engine():
    download_model_artefacts()

    match settings.search_engine:
        case "sparse":
            from .models.sparse_model import SparseSearchEngine

            model = SparseSearchEngine()
        case "dense":
            from .models.dense_model import DenseSearchEngine

            model = DenseSearchEngine(settings.search_model)
        case "hybrid":
            from .models.hybrid_model import HybridSearchEngine

            model = HybridSearchEngine(settings.search_model)

    model.load(settings.search_index)

    return model
