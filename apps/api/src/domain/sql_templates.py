SQL_TEMPLATES = {

    "asset_count": (
        "You have {value} assets in your inventory.",
        "SELECT COUNT(*) FROM Assets WHERE Status <> 'Disposed';"
    ),

    "assets_by_site": (
        "Here is the asset count by site.",
        """
        SELECT s.SiteName, COUNT(*) 
        FROM Assets a
        JOIN Sites s ON s.SiteId = a.SiteId
        WHERE a.Status <> 'Disposed'
        GROUP BY s.SiteName;
        """
    ),

    "asset_value_by_site": (
        "Here is the total asset value per site.",
        """
        SELECT s.SiteName, SUM(a.Cost)
        FROM Assets a
        JOIN Sites s ON s.SiteId = a.SiteId
        WHERE a.Status <> 'Disposed'
        GROUP BY s.SiteName;
        """
    ),

    "assets_purchased_this_year": (
        "Assets purchased this year.",
        """
        SELECT COUNT(*)
        FROM Assets
        WHERE YEAR(PurchaseDate) = YEAR(SYSUTCDATETIME());
        """
    ),

    "assets_by_category": (
        "Assets by category.",
        """
        SELECT Category, COUNT(*)
        FROM Assets
        WHERE Status <> 'Disposed'
        GROUP BY Category;
        """
    ),

    "top_vendor_assets": (
        "Top vendor by asset count.",
        """
        SELECT TOP 1 v.VendorName, COUNT(*)
        FROM Assets a
        JOIN Vendors v ON v.VendorId = a.VendorId
        GROUP BY v.VendorName
        ORDER BY COUNT(*) DESC;
        """
    ),

    "billed_last_quarter": (
        "Total billed last quarter.",
        """
        SELECT SUM(TotalAmount)
        FROM Bills
        WHERE BillDate >= DATEADD(QUARTER, DATEDIFF(QUARTER, 0, SYSUTCDATETIME()) - 1, 0)
          AND BillDate < DATEADD(QUARTER, DATEDIFF(QUARTER, 0, SYSUTCDATETIME()), 0);
        """
    ),

    "open_purchase_orders": (
        "Open purchase orders.",
        "SELECT COUNT(*) FROM PurchaseOrders WHERE Status = 'Open';"
    ),

    "sales_orders_last_month_by_customer": (
        "Sales orders last month for customer.",
        """
        SELECT COUNT(*)
        FROM SalesOrders so
        JOIN Customers c ON c.CustomerId = so.CustomerId
        WHERE c.CustomerCode = @CustomerCode
          AND so.SODate >= DATEADD(MONTH, DATEDIFF(MONTH, 0, SYSUTCDATETIME()) - 1, 0)
          AND so.SODate < DATEADD(MONTH, DATEDIFF(MONTH, 0, SYSUTCDATETIME()), 0);
        """
    )
}