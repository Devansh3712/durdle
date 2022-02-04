PY = venv\Scripts\python
PIP = venv\Scripts\pip

all = run

run:
	$(PY) main.py

install:
	$(PIP) install poetry pyclean >> NUL 2>&1
	$(PY) -m poetry install

requirements:
	$(PY) -m poetry export -f requirements.txt --output requirements.txt --without-hashes

test:
	$(PY) -m pytest -v

clean:
	$(PY) -m pyclean .

.PHONY: clean
