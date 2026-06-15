.PHONY: compose-engine-rebuild

compose-engine-rebuild:
	docker compose --profile engine rm -sf engine queue mongo
	docker compose --profile engine up --build --force-recreate engine queue mongo
