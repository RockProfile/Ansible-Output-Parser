dist:
	pip install .[test]
	python setup.py bdist

linting:
	pip install .[test]
	flake8

test:
	pip install .[test]
	pytest

type-checking:
	pip install .[test]
	mypy .
