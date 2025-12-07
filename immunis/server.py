# src/immunis_cli/server.py
import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException

from .core import set_status
from .schemas import DatadogWebhookPayload, SystemStatus

app = FastAPI(title="Immunis Webhook Listener")


@app.post("/webhook/trigger-lockdown")
async def trigger_lockdown(payload: DatadogWebhookPayload):
    """
    Receives an alert from Datadog and activates system lockdown.
    FastAPI uses the Pydantic model to validate the incoming request body.
    """
    print(f"DATADOG ALERT RECEIVED: {payload.event_title}")
    set_status(SystemStatus(lock_down_mode=True))
    return {"status": "System locked down successfully."}


@app.get("/api/reset", status_code=200)
def reset_lockdown():
    """An endpoint to manually reset the lockdown for demo purposes."""
    set_status(SystemStatus(lock_down_mode=False))
    return {"status": "System lockdown has been reset."}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
