#!/bin/sh

cd /app

# إجراء الهجرات
uv run python manage.py makemigrations
uv run python manage.py migrate

# جمع الملفات الثابتة
uv run python manage.py collectstatic --no-input

# تشغيل الخادم (قد ترغب في ربطه بكل الشبكات وليس فقط localhost)
uv run python manage.py runserver 0.0.0.0:8000
