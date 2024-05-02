FROM python:3.11

RUN pip install poetry

COPY . /app
WORKDIR /app

COPY rest_api/pyproject.toml rest_api/poetry.lock /app/
RUN poetry install

CMD ["poetry", "run", "python", "main.py"]
