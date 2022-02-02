PY = python

all = run

run:
	$(PY) main.py

clean:
	pyclean .

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

install:
	pip install -r requirements.txt
