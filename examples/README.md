# Examples

## Minimal DRF Project

This example shows a tiny Django project using `drf_pyseto` for authentication.

### Setup

```bash
cd examples/minimal
python -m venv .venv
source .venv/bin/activate
pip install -e "../..[test]"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Get Tokens

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"<user>","password":"<pass>"}'
```

### Call Protected Endpoint

```bash
curl http://127.0.0.1:8000/whoami/ \
  -H "Authorization: Bearer <access>"
```
