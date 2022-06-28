#!/bin/bash
source /home/rami/englishquiz/venv/bin/activate
python /home/rami/englishquiz/manage.py publish_scheduled_pages --settings=config.settings.production
