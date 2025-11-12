FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системні залежності для збирання mysqlclient
# (pkg-config + dev-бібліотеки MariaDB/MySQL)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      pkg-config \
      libmariadb-dev \
 && rm -rf /var/lib/apt/lists/*

# Python-залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код проєкту
COPY app/ /app/

# Налаштування Django/ASGI
ENV DJANGO_SETTINGS_MODULE=blog.settings

# Порт (для наочності; docker-compose все одно пробросить)
EXPOSE 8000

# Запуск через uvicorn
CMD ["uvicorn", "blog.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
