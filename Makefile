install:
	poetry install --without dev

install-dev:
	poetry install

lint:
	poetry run ruff check yalchat_server/
	poetry run mypy yalchat_server/


run:
	poetry run uvicorn yalchat_server.app:app --reload
