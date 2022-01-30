PY = python

all = run

run:
	$(PY) -m src.main

clean:
	pyclean .

lint:
	mypy src

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
