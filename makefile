.PHONY: create install setup run clean

VENV_PATH=venv

create:
	python3.10 -m venv $(VENV_PATH)

install:
	$(VENV_PATH)/bin/pip install -r requirements.txt
	$(VENV_PATH)/bin/pip install -e . --use-pep517 --no-deps

setup: create install

run:
	$(VENV_PATH)/bin/python demo/manage.py runserver --insecure 0.0.0.0:8000

clean:
	rm -rf $(VENV_PATH)
