.PHONY: install lint test docs build exe clean

install:
	pip install -e .[dev]

lint:
	ruff avatar_toolkit tests

format:
	black avatar_toolkit tests

test:
	pytest -q

docs:
	sphinx-build -b html docs docs/_build/html

build:
	python -m build

exe:
	pyinstaller avatar_toolkit.spec

clean:
	rm -rf build dist *.egg-info docs/_build
