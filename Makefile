.PHONY: build up stop status report clean

build:
	docker compose build --no-cache

tests:
	docker compose run --build --rm agent

report:
	docker compose up -d allure
	@sleep 2 && (xdg-open http://localhost:8080/latest-report)

status:
	docker compose ps

stop:
	docker compose down

clean:
	rm -rf ./reportallure/*
