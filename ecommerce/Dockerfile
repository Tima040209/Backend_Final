FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && apt-get clean

# Копирование зависимостей
COPY requirements.txt /app/

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . /app/

# Выполнение миграций и сбор статических файлов


CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.wsgi:application"]
