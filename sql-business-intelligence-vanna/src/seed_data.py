"""Create a deterministic synthetic Superstore-style demo dataset."""
import random
from datetime import date, timedelta
from src.database import initialise_database, get_connection

PRODUCTS = [
    ("Furniture", "Chairs", "Ergonomic Office Chair", 180.0),
    ("Furniture", "Tables", "Compact Writing Desk", 240.0),
    ("Office Supplies", "Binders", "Premium Binder Set", 18.0),
    ("Office Supplies", "Storage", "Desktop Storage Box", 32.0),
    ("Technology", "Phones", "Business Smartphone", 520.0),
    ("Technology", "Accessories", "Wireless Keyboard", 45.0),
    ("Technology", "Machines", "Laser Printer", 310.0),
    ("Office Supplies", "Paper", "Recycled Copy Paper", 12.0),
]
REGIONS = ["North", "South", "East", "West"]
CITIES = {
    "North": [("Delhi", "Delhi"), ("Chandigarh", "Chandigarh")],
    "South": [("Bengaluru", "Karnataka"), ("Chennai", "Tamil Nadu")],
    "East": [("Kolkata", "West Bengal"), ("Bhubaneswar", "Odisha")],
    "West": [("Mumbai", "Maharashtra"), ("Pune", "Maharashtra")],
}
CUSTOMERS = [
    ("C001", "Aarav Sharma", "Consumer"),
    ("C002", "Diya Patel", "Corporate"),
    ("C003", "Kabir Rao", "Home Office"),
    ("C004", "Anaya Iyer", "Consumer"),
    ("C005", "Vivaan Das", "Corporate"),
    ("C006", "Meera Nair", "Home Office"),
    ("C007", "Ishaan Gupta", "Consumer"),
    ("C008", "Sara Khan", "Corporate"),
]

def main():
    random.seed(42)
    initialise_database()
    rows = []
    start = date(2025, 1, 1)
    for i in range(1, 501):
        order_day = start + timedelta(days=random.randint(0, 364))
        ship_day = order_day + timedelta(days=random.randint(1, 6))
        region = random.choice(REGIONS)
        city, state = random.choice(CITIES[region])
        category, subcat, product, unit_price = random.choice(PRODUCTS)
        customer_id, customer_name, segment = random.choice(CUSTOMERS)
        quantity = random.randint(1, 8)
        discount = random.choice([0.0, 0.05, 0.10, 0.15, 0.20])
        sales = round(unit_price * quantity * (1 - discount), 2)
        profit = round(sales * random.uniform(-0.12, 0.28), 2)
        rows.append((
            i, f"ORD-{order_day.year}-{i:05d}", order_day.isoformat(),
            ship_day.isoformat(), random.choice(["Standard", "Second Class", "First Class"]),
            customer_id, customer_name, segment, "India", city, state,
            str(random.randint(100000, 999999)), region, f"P{PRODUCTS.index((category, subcat, product, unit_price))+1:03d}",
            category, subcat, product, sales, quantity, discount, profit
        ))
    with get_connection() as conn:
        conn.execute("DELETE FROM orders")
        conn.executemany("""
            INSERT INTO orders (
                row_id, order_id, order_date, ship_date, ship_mode, customer_id,
                customer_name, segment, country, city, state, postal_code, region,
                product_id, category, sub_category, product_name, sales, quantity,
                discount, profit
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, rows)
    print(f"Created data/business.db with {len(rows)} synthetic order rows.")

if __name__ == "__main__":
    main()
