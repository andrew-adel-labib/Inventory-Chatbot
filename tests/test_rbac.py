import unittest
from apps.api.src.domain.authorization import is_authorized


class TestRBAC(unittest.TestCase):

    def test_viewer_permissions(self):
        self.assertTrue(is_authorized("viewer", "asset_count"))
        self.assertFalse(is_authorized("viewer", "billed_last_quarter"))

    def test_admin_permissions(self):
        self.assertTrue(is_authorized("admin", "asset_count"))
        self.assertTrue(is_authorized("admin", "billed_last_quarter"))


if __name__ == "__main__":
    unittest.main()