.PHONY: \
	init test clean \
	clean_unit lint \
	flask_run flask_debug \
	activate

init:
	python3 -m pip install -r requirements.txt

test:
	python3 -m unittest -vb tests/*.py

clean: clean_unit
	rm -rf tests/__pycache__

clean_unit:
	python3 -m clean_unit_tests

lint:
	python3 -m black minerva

flask_run:
	export FLASK_APP=server.py && cd minerva && flask run

flask_debug:
	export FLASK_ENV=development
	make flask_run