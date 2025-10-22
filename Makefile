.PHONY: up down admin migrate bash logs build rebuild clean shell test

# Запуск контейнеров в фоновом режиме
up:
	docker-compose up -d

# Остановка всех контейнеров
down:
	docker-compose down

# Создание суперпользователя admin
admin:
	docker-compose exec web python bz/manage.py createsuperuser --noinput

# Запуск миграций
migrate:
	docker-compose exec web python bz/manage.py makemigrations
	docker-compose exec web python bz/manage.py migrate

# Войти в контейнер web (bash)
bash:
	docker-compose exec web bash

# Просмотр логов
logs:
	docker-compose logs -f

# Сборка контейнеров
build:
	docker-compose build

# Пересборка и запуск
rebuild:
	docker-compose up -d --build

# Полная очистка (контейнеры + volumes)
clean:
	docker-compose down -v

# Открыть Django shell
shell:
	docker-compose exec web python bz/manage.py shell

# Запуск тестов
test:
	docker-compose exec web python bz/manage.py test

# Создание виртуального окружения
venv:
	python -m venv venv