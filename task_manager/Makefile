SHELL := /bin/bash
.PHONY: run setup seed reset-db clean

run:
	source venv/bin/activate && python run.py

setup:
	bash setup.sh

seed:
	source venv/bin/activate && python seed.py

reset-db:
	rm -f app.db
	source venv/bin/activate && python seed.py

clean:
	rm -rf venv app.db __pycache__ **/__pycache__
