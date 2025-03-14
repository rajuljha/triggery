FROM python:3.10.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && \
    apt -y upgrade && \
    apt install -y curl make --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /triggery

WORKDIR /triggery

RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "triggery.wsgi:application"]
