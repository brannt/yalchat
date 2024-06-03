PORT ?= 8000
WORKERS ?= 1
install-pro:
	poetry install --without dev --with deploy

install-dev:
	poetry install

lint:
	poetry run ruff check yalchat_server/
	poetry run mypy yalchat_server/


run-dev:
	poetry run uvicorn yalchat_server.app:app --reload --port $(PORT)

run-pro:
	poetry run gunicorn -w $(WORKERS) -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$(PORT) --preload yalchat_server.app:app
