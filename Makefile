
test: check

check: lint
	pytest

lint:
	ruff check
