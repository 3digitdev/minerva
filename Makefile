.PHONY: \
	init test clean \
	clean_unit lint \
	flask_run deploy

init:
	@python3 -m pip install -r requirements.txt
	@python3 -m init_mongo

test:
	@python3 -m unittest -vb tests/*.py

clean: clean_unit
	rm -rf tests/__pycache__

clean_unit:
	@python3 clean_unit_tests

lint:
	@python3 -m black .

flask_run:
	@export FLASK_APP=minerva && flask run

deploy:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml down -v
	docker-compose -f docker-compose.yml up -d --force-recreate