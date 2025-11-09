# Notification Service (prototype)

Simple FastAPI prototype microservice that accepts a message and either an email or phone number and logs a "Message sent to ..." line with the identifier masked. No real SMS or email is sent — this is only a prototype.

Quick start

1. Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

3. Run the service:

```bash
uvicorn main:app --reload
```

The OpenAPI/Swagger UI is available at: http://127.0.0.1:8000/docs

API

POST /notify
- JSON body:
  - email (optional)
  - phone (optional)
  - message (required)

Response example (prototype):

```json
{
  "status": "ok",
  "sent_to": "a***e@example.com",
  "message": "Message sent (prototype)"
}
```

Testing

Run tests with:

```bash
pytest -q
```

Notes
- Identifiers are masked in logs and responses.
- This repo is a minimal prototype and not production-ready.

Docker

Build the image:

```bash
docker build -t notification-prototype:latest .
```

Run the container (serves on 0.0.0.0:8000):

```bash
docker run --rm -p 8000:8000 notification-prototype:latest
```

You can then open the Swagger UI at http://127.0.0.1:8000/docs
# scalable-services-notification-service