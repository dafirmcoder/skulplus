web: python manage.py migrate --noinput && python scripts/ensure_superuser.py && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
