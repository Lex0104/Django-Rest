FROM python:3.13

RUN pip install poetry

WORKDIR /lms-systems

COPY README.md .

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "env && poetry run python manage.py migrate && poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000"]