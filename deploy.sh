#!/bin/bash
source `which virtualenvwrapper.sh`
workon pyflakes
pip install -U -r requirements.txt
cp wsgi_file_template.py /var/www/pyflakes*_wsgi.py