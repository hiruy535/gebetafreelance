web: daphne mysite.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
heroku addons:create heroku-redis
heroku ps:scale web=1:free worker=1:free

