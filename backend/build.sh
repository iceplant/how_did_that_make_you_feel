#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Download NLTK data
python nltk_setup.py

python manage.py collectstatic --no-input
python manage.py migrate