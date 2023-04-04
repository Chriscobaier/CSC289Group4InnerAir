SRC=wsgi.py
ARGS=run
DEBUG=--debug
CREATE_ADMIN= create_admin
VENV = $(CURDIR)/venv
PYTHON = $(VENV)/bin/python3.11
PIP = $(VENV)/bin/pip3.11

.PHONY: run clean

ifeq ($(OS), Windows_NT)

run: $(VENV)/bin/activate
	$(PYTHON) $(SRC) $(ARGS) $(DEBUG)

admin: $(VENV)/bin/activate
	$(PYTHON) $(SRC) $(CREATE_ADMIN)

$(VENV)/bin/activate: requirements.txt
	python3.11 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test:
	python3.11 -m pytest tests

clean:
	rd /s /q __pycache__
	rd /s /q $(VENV)

else

run: $(VENV)/bin/activate
	$(PYTHON) $(SRC) $(ARGS) --debug

admin: $(VENV)/bin/activate
	$(PYTHON) $(SRC) $(CREATE_ADMIN)


$(VENV)/bin/activate: requirements.txt
	python3.11 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test:
	python3.11 -m pytest tests

clean:
	$(RM) -rf __pycache__
	$(RM) -rf $(VENV)

endif