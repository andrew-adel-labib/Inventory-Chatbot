import time
from app_logging import get_logger
from config import SESSION_TTL_SECONDS

logger = get_logger(__name__)


class SessionStore:
    def __init__(self):
        self._sessions = {}

    def save(self, session_id, messages):
        self._sessions[session_id] = {
            "messages": list(messages),
            "timestamp": time.time(),
        }

    def get(self, session_id):
        entry = self._sessions.get(session_id)
        if not entry:
            return []

        if time.time() - entry["timestamp"] > SESSION_TTL_SECONDS:
            logger.info("Session expired: %s", session_id)
            del self._sessions[session_id]
            return []

        return list(entry["messages"])