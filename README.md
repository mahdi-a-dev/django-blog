# Django Blog

A blog application built with **Django 6.1** and **Django REST Framework**.

Users sign up with an email address, staff write and edit posts, superusers publish and delete them, and everyone can comment.

## Stack

Django 6.1.2 · DRF 3.18.3 · PostgreSQL 17 · Pillow · psycopg3 · python-decouple

## Setup

```bash
cp .env.example .env      # fill in SECRET_KEY, database and email settings
docker compose up --build
```


Run locally without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# in .env set POSTGRES_HOST=localhost
cd core
python manage.py migrate
python manage.py runserver
```


## Roles

| Actions | Anonymous | User | Staff | Superuser |
|---|:-:|:-:|:-:|:-:|
| Read published posts | ✅ | ✅ | ✅ | ✅ |
| Comment / reply | | ✅ | ✅ | ✅ |
| Create / edit posts | | | ✅ | ✅ |
| Publish / delete posts | | | | ✅ |

## Layout

```
core/
├── core/        project settings and root URLs
├── accounts/    custom email user model, auth, profiles
├── blog/        posts, categories, comments
│   └── api/     REST API (admin only)
├── static/      css and images
└── templates/   base, accounts, blog
```

## API

`/api/post/` and `/api/post/<pk>/` — GET, POST, PUT, DELETE. Admin users only.
Browsable API at `/api-auth/`.

## License

MIT
