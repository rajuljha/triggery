serve:
	gunicorn triggery.wsgi:application -c gunicorn.conf.py

worker:
	celery -A triggery worker -l INFO

beat:
	celery -A triggery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

collectstatic:
	python manage.py collectstatic

migrate:
	python manage.py migrate
