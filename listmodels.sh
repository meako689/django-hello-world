#!/usr/bin/env bash
now=$(date +"%d_%m_%Y")
python manage.py listmodels 2>./"$now".dat
