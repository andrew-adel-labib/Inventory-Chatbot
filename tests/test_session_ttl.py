import unittest
from apps.api.src.infra.session_store import SessionStore


class TestSessionTTL(unittest.TestCase):

    def test_session_ttl_eviction(self):
        store = SessionStore()

        store.save("s1", ["msg"])
        store._sessions["s1"]["timestamp"] -= 9999

        result = store.get("s1")

        self.assertNotIn("s1", store._sessions)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()