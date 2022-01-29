PY = python

all = run

run:
	$(PY) -m src.main

clean:
	pyclean .

lint:
	mypy .
