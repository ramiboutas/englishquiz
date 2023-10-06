#!/bin/bash
cd /home/rami/englishquiz
source venv/bin/activate
python manage.py dbbackup
mkdir /home/rami/backups/englishquiz/$(date +%Y-%m-%d)
python manage.py dumpdata > /home/rami/backups/englishquiz/$(date +%Y-%m-%d)/db.json
