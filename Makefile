include .env

.PHONY: help dc-start dc-stop dc-start-local dc-build dc-clean

help: ## Show this help menu
	@echo "Usage: make [TARGET ...]"
	@echo ""
	@grep --no-filename -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

dc-clean: ## Ensure no docker containers are running (might need sudo)
	@docker-compose stop;

dc-stop: ## Stop docker (might need sudo)
	@docker-compose stop;

dc-start: dc-clean dc-build ## Start docker (might need sudo)
	@docker-compose up -d;

dc-start-verbose: dc-clean dc-build ## Start docker with messages
	@docker-compose up;

dc-build:
	@docker-compose build;