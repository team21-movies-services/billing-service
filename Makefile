

create_network:
	@docker network create billing-service-network 2>/dev/null || echo "billing-service-network is up-to-date"

create_test_network:
	@docker network create test-billing-service-network 2>/dev/null || echo "test-billing-service-network is up-to-date"

#react build
.PHONY: react
react:
	cd frontend && npm run build

# prod start
.PHONY: up
up: create_network ## up services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml up -d

.PHONY: logs
logs: ## tail logs services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml down

.PHONY: build
build: ## build services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml build

.PHONY: restart
restart: down up ## restart services

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml down --remove-orphans --volumes
# prod end

# local start

.PHONY: up-local
up-local: create_network react ## up local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.override.yml up --build

.PHONY: down-local
down-local: ## down local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.override.yml down

.PHONY: build-local
build-local: ## build local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.override.yml build --force-rm

.PHONY: build-force-local
build-force-local: ## build force services
	@docker-compose -f docker-compose.local.yml -f docker-compose.override.yml build --no-cache

.PHONY: logs-local
logs-local: ## logs local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.override.yml logs -f

.PHONY: restart-local
restart-local: down-local up-local ## logs local services

.PHONY: uninstall-local
uninstall-local: ## uninstall local services
	@docker-compose -f docker-compose.override.yml -f docker-compose.local.yml down --remove-orphans --volumes

# local end

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# test start
.PHONY: up-test
up-test: create_test_network ## up test services
	@docker-compose -p test_billing_service -f docker-compose.test.yml up --build


.PHONY: down-test
down-test: ## down test services
	@docker-compose -p test_billing_service -f docker-compose.test.yml down

.PHONY: run-test
run-test: create_test_network ## run and uninstall tests services
	@docker-compose -p test_billing_service -f docker-compose.test.yml up --build

.PHONY: run-test-d
run-test-d: create_test_network ## run and uninstall tests services
	@docker-compose -p test_billing_service -f docker-compose.test.yml up --build -d

.PHONY: build-test
build-test: create_test_network
	@docker-compose -p test_billing_service -f docker-compose.test.yml build --force-rm

.PHONY: logs-test
logs-test: ## logs test services
	@docker-compose -p test_billing_service -f docker-compose.test.yml logs -f

.PHONY: pytest-logs
pytest-logs:
	@docker-compose -p test_billing_service -f docker-compose.test.yml logs test-billing-service-api -f

.PHONY: uninstall-test
uninstall-test: ## uninstall test services
	@docker-compose -p test_billing_service -f docker-compose.test.yml down --remove-orphans --volumes

.PHONY: all-test
all-test: run-test-d pytest-logs uninstall-test
# test end
