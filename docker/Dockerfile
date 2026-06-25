FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/docker/entrypoint-app.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
