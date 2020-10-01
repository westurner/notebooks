
default: test

test:
	pytest --with-cov ./basechange.py

coverage:
	pytest --cov=basechange --cov-report=term-missing ./basechange.py

all: test
