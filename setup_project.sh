#!/bin/bash

set -e

echo "🚀 Запуск установки проекта BZ"

# Проверка и установка Docker
if ! command -v docker &> /dev/null; then
    echo "Установка Docker..."
    sudo pacman -Sy --noconfirm docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    newgrp docker
fi

# Запуск PostgreSQL в Docker
echo "Запуск PostgreSQL..."
docker run --name postgres-bz \
  -e POSTGRES_DB=bz_database \
  -e POSTGRES_USER=bz_user \
  -e POSTGRES_PASSWORD=bz_password \
  -p 5432:5432 \
  -d postgres:15

# Ожидание запуска PostgreSQL
sleep 5

# Настройка Django
echo "Настройка Django..."
cd ~/bz
source venv/bin/activate
cd bz

# Миграции базы данных
echo "Применение миграций..."
python manage.py migrate

# Создание суперпользователя
echo "Создание суперпользователя..."
python manage.py createsuperuser --noinput || true

# Запуск сервера
echo "Запуск сервера Django..."
echo "📱 Сайт доступен по адресу: http://127.0.0.1:8000"
python manage.py runserver