.PHONY: init test lint flask_run flask_debug activate

init:
	python3 -m pip install -r requirements.txt

test:
	# TODO

lint:
	python3 -m black minerva

flask_run:
	export FLASK_APP=server.py && cd minerva && flask run

flask_debug:
	export FLASK_ENV=development
	make flask_run

activate:
	. venv/bin/activate
