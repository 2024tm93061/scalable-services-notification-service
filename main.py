from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = FastAPI(title="Notification Service", description="Prototype notification microservice", version="0.1")


class NotifyRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    message: str


def mask_email(email: str) -> str:
    try:
        local, domain = email.split("@", 1)
    except Exception:
        return "***@***"
    if len(local) <= 2:
        masked_local = local[0] + "*" * max(0, len(local) - 1)
    else:
        masked_local = local[0] + "*" * max(0, len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"


def mask_phone(phone: str) -> str:
    # keep only digits, mask all but last 2 digits
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        return "**"
    if len(digits) <= 2:
        return "*" * len(digits)
    return "*" * (len(digits) - 2) + digits[-2:]


@app.post("/notify")
def notify(req: NotifyRequest):
    # simple validation: require either email or phone
    if not req.email and not req.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    if req.email:
        masked = mask_email(req.email)
        target = masked
    else:
        masked = mask_phone(req.phone)
        target = masked

    # Prototype only: do not actually send messages. Just log.
    logging.info(f"Message sent to {target}: {req.message}")

    # Return a small, test-friendly response including the masked target
    return {"status": "ok", "sent_to": target, "message": "Message sent (prototype)"}
