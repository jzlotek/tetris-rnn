SHELL=/bin/bash

.PHONY: clean run

venv:
	bash install.sh

clean:
	rm -rfv venv __pycache__ **/__pycache__ *.json *.png

run-%: src/%.py venv
	source ./venv/bin/activate && \
		python src/$*.py ${ARGS}

data:
	source ./venv/bin/activate && \
		python src/datatools.py --combine default

model-play:
	source ./venv/bin/activate && \
		python src/main.py --model model.h5

