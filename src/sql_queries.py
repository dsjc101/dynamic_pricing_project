# To Store SQL Queries for Reuse
monthly_sales_query = """
SELECT strftime('%Y-%m', InvoiceDate) AS Month, 
       SUM(Quantity * UnitPrice) AS TotalSales
FROM transactions
GROUP BY Month
ORDER BY Month;
"""

top_products_query = """
SELECT Description, 
       SUM(Quantity * UnitPrice) AS Revenue
FROM transactions
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 10;
"""

return_rate_query = """
SELECT Description,
       SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END) AS ReturnCount,
       COUNT(*) AS TotalOrders,
       ROUND(1.0 * SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS ReturnRate
FROM transactions
GROUP BY Description
HAVING TotalOrders > 50
ORDER BY ReturnRate DESC
LIMIT 10;
"""

avg_order_value_query = """
SELECT Country, 
       ROUND(SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo), 2) AS AvgOrderValue
FROM transactions
GROUP BY Country
ORDER BY AvgOrderValue DESC;
"""
