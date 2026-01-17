import json
import time
import urllib.request

from app_logging import get_logger
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_KEY,
)

logger = get_logger(__name__)

API_VERSION = "2024-12-01-preview"


def classify_intent(messages):
    url = (
        f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/"
        f"{AZURE_OPENAI_DEPLOYMENT}/chat/completions"
        f"?api-version={API_VERSION}"
    )

    payload = {
        "messages": messages,
        "temperature": 0,
        "max_tokens": 64,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY,
        },
    )

    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
    except Exception:
        logger.exception("Azure OpenAI request failed")
        raise RuntimeError("Azure OpenAI request failed")

    latency_ms = int((time.monotonic() - start) * 1000)
    return body, latency_ms