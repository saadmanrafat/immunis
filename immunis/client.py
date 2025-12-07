from google import genai
from .config import settings


def _get_client() -> genai.Client:
    return genai.Client(api_key=settings.google_api_key.get_secret_value())


client = _get_client()
