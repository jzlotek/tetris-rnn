SHELL=/bin/bash

.PHONY: clean run

venv:
	bash install.sh

clean:
	rm -rf venv __pycache__

run: venv
	source ./venv/bin/activate && \
		python src/main.py
