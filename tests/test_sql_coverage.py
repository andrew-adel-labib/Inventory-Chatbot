from apps.api.src.domain.sql_templates import SQL_TEMPLATES

def test_all_required_intents_present():
    required_intents = {
        "asset_count",
        "assets_by_site",
        "asset_value_by_site",
        "assets_purchased_this_year",
        "assets_by_category",
        "top_vendor_assets",
        "billed_last_quarter",
        "open_purchase_orders",
        "sales_orders_last_month_by_customer",
    }

    assert required_intents.issubset(SQL_TEMPLATES.keys())