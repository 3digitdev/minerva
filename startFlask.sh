#!/usr/bin/env bash

python3 -m pip install -r requirements.txt
export FLASK_APP=minerva
flask run --host=0.0.0.0