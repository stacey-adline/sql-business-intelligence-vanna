from src.database import get_connection
from src.vanna_client import create_vanna_client

DDL = """
CREATE TABLE orders (
    row_id INTEGER PRIMARY KEY,
    order_id TEXT,
    order_date TEXT,
    ship_date TEXT,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL
);
"""

DOCUMENTATION = """
The orders table contains one row per order line.
sales is the net sales amount after discount.
profit is the profit amount and can be negative.
discount is a decimal fraction, for example 0.10 means 10 percent.
order_date and ship_date use ISO format YYYY-MM-DD.
The dataset is synthetic Indian retail demo data covering 2025.
Use SUM(sales) for total sales, SUM(profit) for total profit,
COUNT(DISTINCT order_id) for order count, and AVG(discount) for average discount.
"""

def main():
    vn = create_vanna_client()
    vn.train(ddl=DDL)
    vn.train(documentation=DOCUMENTATION)
    examples = [
        ("What is the total sales amount?", "SELECT ROUND(SUM(sales), 2) AS total_sales FROM orders;"),
        ("What is the total profit?", "SELECT ROUND(SUM(profit), 2) AS total_profit FROM orders;"),
        ("Show sales by region.", "SELECT region, ROUND(SUM(sales), 2) AS total_sales FROM orders GROUP BY region ORDER BY total_sales DESC;"),
        ("Which five products have the highest sales?", "SELECT product_name, ROUND(SUM(sales), 2) AS total_sales FROM orders GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;"),
        ("Which category has the highest profit?", "SELECT category, ROUND(SUM(profit), 2) AS total_profit FROM orders GROUP BY category ORDER BY total_profit DESC LIMIT 1;"),
        ("Show monthly sales for 2025.", "SELECT strftime('%Y-%m', order_date) AS month, ROUND(SUM(sales), 2) AS sales FROM orders GROUP BY month ORDER BY month;"),
        ("Which are the top five customers by sales?", "SELECT customer_name, ROUND(SUM(sales), 2) AS total_sales FROM orders GROUP BY customer_name ORDER BY total_sales DESC LIMIT 5;"),
        ("How many orders are there in each region?", "SELECT region, COUNT(DISTINCT order_id) AS order_count FROM orders GROUP BY region ORDER BY order_count DESC;"),
        ("What is the average discount by category?", "SELECT category, ROUND(AVG(discount) * 100, 2) AS avg_discount_percent FROM orders GROUP BY category;"),
        ("Which sub-category has the lowest total profit?", "SELECT sub_category, ROUND(SUM(profit), 2) AS total_profit FROM orders GROUP BY sub_category ORDER BY total_profit ASC LIMIT 1;"),
    ]
    for question, sql in examples:
        vn.train(question=question, sql=sql)
    print("Vanna training completed: schema, documentation, and 10 example queries.")

if __name__ == "__main__":
    main()
