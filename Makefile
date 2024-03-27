
test: check

check: lint
	python3 -m unittest

lint:
	flake8

version:
	git describe --dirty --tags > ./version

.PHONY: version
