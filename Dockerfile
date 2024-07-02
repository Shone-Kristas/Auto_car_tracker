FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

WORKDIR /app/CarLogicDjango

CMD python manage.py migrate && \
    python manage.py collectstatic --no-input && \
    python manage.py runserver 0.0.0.0:8000

