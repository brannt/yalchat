install-pro:
	poetry install --without dev --with deploy

install-dev:
	poetry install

lint:
	poetry run ruff check yalchat_server/
	poetry run mypy yalchat_server/


run-dev:
	poetry run uvicorn yalchat_server.app:app --reload

run-pro:
	poetry run gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 yalchat_server.app:app
