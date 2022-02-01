PY = python

all = run

run:
	$(PY) main.py

clean:
	pyclean .

lint:
	mypy durdle

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
