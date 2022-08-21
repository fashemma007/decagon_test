setup:
	@python3 -m venv .venv
	@. .venv/bin/activate

install:
	@.venv/bin/pip install -r requirements.txt

lint:
	@pylint --load-plugins pylint_flask --disable=R,C *.py

run:
	@.venv/bin/python main.py