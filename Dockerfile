FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

WORKDIR /app/CarLogicDjango

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate && \
    gunicorn CarLogicDjango.wsgi:application --bind 0.0.0.0:8000

