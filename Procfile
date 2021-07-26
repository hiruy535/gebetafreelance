web: daphne mysite.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
heroku addons:create heroku-redis
export DJANGO_SETTINGS_MODULE=mysite.settings
heroku ps:scale web=1 worker=1
heroku config:set DJANGO_SETTINGS_MODULE=mysite.settings --account personal


