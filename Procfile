web: gunicorn mysite.asgi:application --log-file -port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
