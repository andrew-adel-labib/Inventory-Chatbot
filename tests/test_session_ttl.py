import time
from apps.api.src.infra.session_store import SessionStore

def test_session_ttl_eviction():
    store = SessionStore()
    store.save("s1", ["msg"])
    store._sessions["s1"]["timestamp"] -= 9999  
    store.get("s1")
    assert "s1" not in store._sessions