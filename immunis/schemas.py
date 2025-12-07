from pydantic import BaseModel, Field


class SystemStatus(BaseModel):
    """
    Represents the current status of system_status.json
    """

    lock_down_mode: bool = False


class GuardDogResponse(BaseModel):
    """
    The expected JSON Response from GuardDog
    """

    score: int = Field(..., ge=0, le=100)
    is_attack: bool
    reason: str


class DatadogWebhookPayload(BaseModel):
    """
    The expected JSON Payload from Datadog Webhook
    """

    event_title: str = Field(..., alias="alert_title")
    event_message: str = Field(..., alias="alert_message")
    event_type: str = Field(..., alias="alert_type")
    event_priority: str = Field(..., alias="alert_priority")
    event_tags: list[str] = Field(..., alias="alert_tags")
    event_url: str = Field(..., alias="alert_url")
