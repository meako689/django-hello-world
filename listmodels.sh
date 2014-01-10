#!/usr/bin/env bash
now=$(date +"%m_%d_%Y")
python manage.py listmodels 2>./"$now".dat
