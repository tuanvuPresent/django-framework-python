release: python manage.py migrate
release: python manage.py loaddata fixtures/*
work: celery -A Example beat -l info -S django
work: celery -A Example worker -l info
web: gunicorn Example.wsgi:application
