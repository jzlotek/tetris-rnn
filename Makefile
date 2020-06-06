SHELL=/bin/bash

.PHONY: clean run

venv:
	bash install.sh

clean:
	rm -rfv venv __pycache__ **/__pycache__

run-%: src/%.py venv
	source ./venv/bin/activate && \
		python src/$*.py
