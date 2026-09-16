import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
CHKPT_DIR = BASE_DIR / "checkpoints"

SearchEngine = Literal["sparse", "dense", "hybrid"]


load_dotenv(BASE_DIR / "config" / ".env")

with open(BASE_DIR / "config" / "config.json", "r") as f:
    CONFIG = json.load(f)


@dataclass(frozen=True)
class Settings:
    allowed_origins: list[str] = field(
        default_factory=lambda: os.environ.get("ALLOWED_ORIGINS", "").split(",")
    )

    search_engine: SearchEngine = CONFIG.get("search_engine")
    search_index: str = Path(
        CHKPT_DIR,
        search_engine,
        CONFIG.get("search_index"),
    ).as_posix()
    search_model: str = Path(CHKPT_DIR, CONFIG.get("search_model")).as_posix()
    search_repo: str = CONFIG.get("search_repo")

    nltk_data: str = CONFIG.get("nltk_data")


settings = Settings()
