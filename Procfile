release: python manage.py migrate

worker: celery -A Example beat -l info -S django
worker: celery -A Example worker -l info
web: gunicorn Example.wsgi:application
