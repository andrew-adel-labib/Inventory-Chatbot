import json
import urllib.request
from apps.api.src.app_logging import get_logger
from apps.api.src.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_KEY,
)

logger = get_logger(__name__)

API_VERSION = "2024-12-01-preview"


def classify_intent(messages):
    if not AZURE_OPENAI_ENDPOINT.startswith("https://"):
        raise RuntimeError("Invalid AZURE_OPENAI_ENDPOINT")

    url = (
        f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}"
        f"/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}"
        f"/chat/completions?api-version={API_VERSION}"
    )

    logger.info("Azure OpenAI URL: %s", url)

    payload = {
        "messages": messages,
        "temperature": 0,
        "max_tokens": 256,
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"], 0
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        logger.error("Azure OpenAI HTTP error %s: %s", e.code, error_body)
        raise RuntimeError("Azure OpenAI request failed")