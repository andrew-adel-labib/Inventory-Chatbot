from app_logging import get_logger

logger = get_logger(__name__)

FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]


def validate_sql(sql: str):
    upper_sql = sql.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper_sql:
            logger.warning("Unsafe SQL detected: %s", keyword)
            raise ValueError("Unsafe SQL detected")