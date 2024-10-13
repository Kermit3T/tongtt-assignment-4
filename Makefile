ifeq ($(OS),Windows_NT)
    PYTHON = python
    VENV = venv
    VENV_BIN = $(VENV)\Scripts
    SEP = &
else
    PYTHON = python3
    VENV = venv
    VENV_BIN = $(VENV)/bin
    SEP = ;
endif

VENV_PYTHON = $(VENV_BIN)\python
VENV_PIP = $(VENV_BIN)\pip

.PHONY: install run clean

$(VENV_BIN)\activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -r requirements.txt

install: $(VENV_BIN)\activate

run: $(VENV_BIN)\activate
	$(VENV_PYTHON) -m flask run --host=0.0.0.0 --port=3000

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete