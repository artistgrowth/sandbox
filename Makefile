.PHONY: help
help: ## help
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install: ## install dependencies
	pip install -r requirements/requirements-dev.txt

.PHONY: test
test: ## run tests and coverage
	mkdir reports || true
	coverage run manage.py test

.PHONY: lint
lint: ## lint files
	pre-commit run --all-files

.PHONY: run
run: ## run
	python manage.py runserver 0.0.0.0:${PORT}
