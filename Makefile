.PHONY: compose-engine-rebuild

compose-engine-rebuild:
	docker compose --profile mongo rm -sf engine queue mongo experiment-management experiments_db infra-management infra_db user-management user_management_db web results-management
	docker compose --profile mongo --profile experiment-management up --build --force-recreate engine mongo experiment-management infra-management user-management web results-management

hard-reset:
	docker stop $$(docker ps -q -a)
	docker rm $$(docker ps -q -a)
	docker system prune --all --volumes --force
	docker volume prune -a --force
