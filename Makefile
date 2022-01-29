PY = python

all = run

run:
	$(PY) -m src.main.py

clean:
	pyclean .

lint:
	mypy .
