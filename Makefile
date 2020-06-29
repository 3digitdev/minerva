.PHONY: init test lint

init:
	pytho3 -m pip install -r requirements.txt

test:
	# TODO

lint:
	python3 -m black minerva
