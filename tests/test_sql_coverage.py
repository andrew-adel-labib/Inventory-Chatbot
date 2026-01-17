import unittest
from apps.api.src.domain.sql_templates import SQL_TEMPLATES


class TestSQLTemplateCoverage(unittest.TestCase):

    def test_all_required_intents_present(self):
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

        self.assertTrue(
            required_intents.issubset(SQL_TEMPLATES.keys()),
            msg="One or more required SQL templates are missing",
        )


if __name__ == "__main__":
    unittest.main()