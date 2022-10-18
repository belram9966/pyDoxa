release: python manage.py migrate; python manage.py loaddata core/fixtures/data_prueba.json;
web: gunicorn pycronos.wsgi