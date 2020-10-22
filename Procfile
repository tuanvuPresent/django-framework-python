release: python manage.py migrate
release: python manage.py loaddata fixtures/*
worker: celery -A Example beat -l info -S django
worker: celery -A Example worker -l info
web: gunicorn Example.wsgi:application
