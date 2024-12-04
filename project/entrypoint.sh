#!/bin/bash

deploy_hard(){
	echo "running hard deploy..."
	python manage.py collectstatic
	python manage.py migrate
	uwsgi --ini uwsgi.ini
}


# Perform a soft deployment of the application.
# This includes collecting static files, applying database migrations,

deploy_soft(){
	echo "running soft deploy.."
	python manage.py collectstatic
	python manage.py migrate	
	uwsgi --ini uwsgi.ini --py-autoreload 1
}


case "${DEPLOY_LEVEL}" in
        hard) deploy_hard ;;
        soft) deploy_soft ;;
	        *) deploy_soft ;;
	esac


	echo "Deploying..."
