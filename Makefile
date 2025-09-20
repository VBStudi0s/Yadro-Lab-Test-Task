docker-test-default:
	@docker-compose up --build --force-recreate

docker-test-stop:
	@docker-compose down
