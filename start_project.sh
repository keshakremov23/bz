#!/bin/bash

set -e

echo "🔄 Запуск проекта BZ..."

# Запуск PostgreSQL с sudo
sudo docker start postgres-bz

# Запуск Django
cd ~/bz
source venv/bin/activate
cd bz

echo "📱 Сервер запускается на http://127.0.0.1:8000"
python manage.py runserver