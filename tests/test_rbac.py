from apps.api.src.domain.authorization import is_authorized

def test_viewer_permissions():
    assert is_authorized("viewer", "asset_count")
    assert not is_authorized("viewer", "billed_last_quarter")

def test_admin_permissions():
    assert is_authorized("admin", "asset_count")
    assert is_authorized("admin", "billed_last_quarter")