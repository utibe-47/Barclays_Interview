#!/bin/sh

# Set environmental variables.
export THERMOS_ENV="dev"

# Run the flask app.
python myapp.py runserver
