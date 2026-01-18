class SessionStore:
    _store = {}

    @classmethod
    def append(cls, session_id, role, message, intent=None):
        cls._store.setdefault(session_id, []).append({
            "role": role,
            "message": message,
            "intent": intent
        })

    @classmethod
    def get(cls, session_id):
        return cls._store.get(session_id, [])