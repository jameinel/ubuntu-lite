
test: check

check: lint
	python3 -m unittest

lint:
	flake8
