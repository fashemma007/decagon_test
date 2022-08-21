setup:
	@python3 -m venv .venv
	@. .venv/bin/activate

install:
	@.venv/bin/pip install -r requirements.txt

run:
	@.venv/bin/python main.py