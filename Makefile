.PHONY: build up stop status

build:
	docker compose build

up: build
	docker compose up -d --force-recreate
	docker compose logs -f agent

status:
	docker compose ps

stop:
	docker compose down
