FROM python:3.12.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY config/config.json ./config/config.json
COPY hscs/api ./hscs/api
COPY pyproject.toml ./

RUN uv pip install --system --no-cache --no-compile . && \
    python -m nltk.downloader -d /usr/local/share/nltk_data wordnet && \
    chmod -R a+rX /usr/local/share/nltk_data && \
    useradd --create-home hscs && \
    mkdir checkpoints && \
    chown hscs /app /app/checkpoints

USER hscs

EXPOSE 8000

CMD ["uvicorn", "hscs.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
