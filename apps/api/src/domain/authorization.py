from apps.api.src.app_logging import get_logger

logger = get_logger(__name__)

ROLE_PERMISSIONS = {
    "viewer": {"asset_count", "assets_by_site"},
    "finance": {"asset_count", "billed_last_quarter"},
    "admin": {"ALL"},
}


def is_authorized(role, intent):
    allowed = ROLE_PERMISSIONS.get(role, set())
    if "ALL" in allowed or intent in allowed:
        return True
    logger.warning("Unauthorized intent '%s' for role '%s'", intent, role)
    return False