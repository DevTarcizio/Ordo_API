FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry  

COPY pyproject.toml poetry.lock* ./


RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

COPY . .

EXPOSE 10000
CMD ["uvicorn", "ordo_fast.app:app", "--host", "0.0.0.0", "--port", "10000"]