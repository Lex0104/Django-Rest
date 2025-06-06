FROM python:3.12-slim

RUN pip install poetry

WORKDIR /lms-systems

COPY README.md .

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]