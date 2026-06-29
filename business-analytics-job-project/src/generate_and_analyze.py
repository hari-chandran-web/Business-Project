from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RANDOM_SEED = 42


def money(value: float) -> float:
    return round(value, 2)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def generate_customers(n: int = 650) -> list[dict]:
    random.seed(RANDOM_SEED)
    cities = [
        ("Mumbai", "India", "West"),
        ("Bengaluru", "India", "South"),
        ("Delhi", "India", "North"),
        ("Hyderabad", "India", "South"),
        ("Toronto", "Canada", "Ontario"),
        ("Vancouver", "Canada", "British Columbia"),
        ("Calgary", "Canada", "Alberta"),
        ("Montreal", "Canada", "Quebec"),
    ]
    channels = ["Organic", "Paid Search", "Social", "Referral", "Marketplace"]
    segments = ["Student", "Young Professional", "Family", "Premium", "Small Business"]

    rows = []
    for idx in range(1, n + 1):
        city, country, region = random.choice(cities)
        signup_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 680))
        rows.append(
            {
                "customer_id": f"C{idx:04d}",
                "signup_date": signup_date.isoformat(),
                "city": city,
                "country": country,
                "region": region,
                "segment": random.choices(segments, weights=[12, 30, 28, 18, 12])[0],
                "acquisition_channel": random.choices(channels, weights=[28, 24, 20, 16, 12])[0],
            }
        )
    return rows


def generate_products() -> list[dict]:
    catalog = [
        ("Wireless Earbuds", "Electronics", 1450, 2999, "China"),
        ("Smart Watch", "Electronics", 2600, 5499, "China"),
        ("Office Chair", "Furniture", 4200, 7999, "India"),
        ("Standing Desk", "Furniture", 8700, 15999, "Canada"),
        ("Running Shoes", "Fashion", 1650, 3999, "Vietnam"),
        ("Winter Jacket", "Fashion", 3200, 8999, "Canada"),
        ("Coffee Maker", "Home", 2100, 4999, "India"),
        ("Air Fryer", "Home", 3100, 6999, "China"),
        ("Notebook Pack", "Stationery", 120, 399, "India"),
        ("Laptop Backpack", "Accessories", 850, 2199, "India"),
        ("Yoga Mat", "Fitness", 450, 1299, "India"),
        ("Protein Shaker", "Fitness", 180, 599, "India"),
    ]
    rows = []
    for idx, (name, category, cost, price, supplier_country) in enumerate(catalog, start=1):
        rows.append(
            {
                "product_id": f"P{idx:03d}",
                "product_name": name,
                "category": category,
                "unit_cost_inr": cost,
                "list_price_inr": price,
                "supplier_country": supplier_country,
            }
        )
    return rows


def generate_orders(customers: list[dict], products: list[dict], n: int = 4200) -> list[dict]:
    random.seed(RANDOM_SEED + 1)
    rows = []
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    days = (end - start).days
    product_lookup = {p["product_id"]: p for p in products}

    for idx in range(1, n + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        order_date = start + timedelta(days=random.randint(0, days))
        quantity = random.choices([1, 2, 3, 4], weights=[62, 25, 9, 4])[0]
        discount_pct = random.choices([0, 5, 10, 15, 20, 25, 30], weights=[30, 18, 18, 14, 10, 6, 4])[0]
        base_delivery = 90 if customer["country"] == "India" else 260
        delivery_cost = base_delivery + random.randint(0, 220)
        promised_days = random.choice([2, 3, 4, 5, 7])
        actual_days = promised_days + random.choices([-1, 0, 1, 2, 3], weights=[10, 48, 24, 12, 6])[0]
        unit_price = product_lookup[product["product_id"]]["list_price_inr"] * (1 - discount_pct / 100)

        rows.append(
            {
                "order_id": f"O{idx:05d}",
                "order_date": order_date.isoformat(),
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "discount_pct": discount_pct,
                "unit_price_inr": money(unit_price),
                "delivery_cost_inr": money(delivery_cost),
                "promised_delivery_date": (order_date + timedelta(days=promised_days)).isoformat(),
                "actual_delivery_date": (order_date + timedelta(days=max(1, actual_days))).isoformat(),
                "payment_method": random.choice(["UPI", "Credit Card", "Debit Card", "Wallet", "PayPal"]),
            }
        )
    return rows


def analyze(customers: list[dict], products: list[dict], orders: list[dict]) -> tuple[list[dict], list[dict]]:
    product_lookup = {row["product_id"]: row for row in products}
    customer_lookup = {row["customer_id"]: row for row in customers}
    monthly = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "gross_profit": 0.0, "sla_breaches": 0})
    segment_profit = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "gross_profit": 0.0})

    latest_order_date = max(date.fromisoformat(row["order_date"]) for row in orders)
    last_customer_order = {}

    for order in orders:
        product = product_lookup[order["product_id"]]
        customer = customer_lookup[order["customer_id"]]
        order_date = date.fromisoformat(order["order_date"])
        month = order["order_date"][:7]
        revenue = float(order["unit_price_inr"]) * int(order["quantity"])
        cogs = float(product["unit_cost_inr"]) * int(order["quantity"])
        gross_profit = revenue - cogs - float(order["delivery_cost_inr"])
        sla_breach = date.fromisoformat(order["actual_delivery_date"]) > date.fromisoformat(order["promised_delivery_date"])

        monthly[month]["orders"] += 1
        monthly[month]["revenue"] += revenue
        monthly[month]["gross_profit"] += gross_profit
        monthly[month]["sla_breaches"] += int(sla_breach)

        key = (customer["country"], customer["segment"])
        segment_profit[key]["orders"] += 1
        segment_profit[key]["revenue"] += revenue
        segment_profit[key]["gross_profit"] += gross_profit

        last_customer_order[order["customer_id"]] = max(last_customer_order.get(order["customer_id"], order_date), order_date)

    monthly_rows = []
    for month, values in sorted(monthly.items()):
        revenue = values["revenue"]
        monthly_rows.append(
            {
                "month": month,
                "orders": values["orders"],
                "revenue_inr": money(revenue),
                "gross_profit_inr": money(values["gross_profit"]),
                "gross_margin_pct": money(values["gross_profit"] / revenue * 100 if revenue else 0),
                "sla_breach_rate_pct": money(values["sla_breaches"] / values["orders"] * 100),
            }
        )

    segment_rows = []
    for (country, segment), values in sorted(segment_profit.items()):
        revenue = values["revenue"]
        segment_rows.append(
            {
                "country": country,
                "segment": segment,
                "orders": values["orders"],
                "revenue_inr": money(revenue),
                "gross_profit_inr": money(values["gross_profit"]),
                "gross_margin_pct": money(values["gross_profit"] / revenue * 100 if revenue else 0),
            }
        )

    churn_rows = []
    for customer_id, last_date in sorted(last_customer_order.items()):
        customer = customer_lookup[customer_id]
        inactive_days = (latest_order_date - last_date).days
        churn_rows.append(
            {
                "customer_id": customer_id,
                "country": customer["country"],
                "segment": customer["segment"],
                "last_order_date": last_date.isoformat(),
                "inactive_days": inactive_days,
                "churn_risk": "High" if inactive_days >= 90 else "Low",
            }
        )

    return monthly_rows, segment_rows, churn_rows


def main() -> None:
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers, products)
    monthly_kpis, segment_profitability, churn_risk = analyze(customers, products, orders)

    write_csv(DATA_DIR / "customers.csv", customers)
    write_csv(DATA_DIR / "products.csv", products)
    write_csv(DATA_DIR / "orders.csv", orders)
    write_csv(DATA_DIR / "monthly_kpis.csv", monthly_kpis)
    write_csv(DATA_DIR / "segment_profitability.csv", segment_profitability)
    write_csv(DATA_DIR / "churn_risk.csv", churn_risk)

    print(f"Created dataset in {DATA_DIR}")
    print(f"Orders: {len(orders):,}")
    print(f"Customers: {len(customers):,}")
    print(f"Products: {len(products):,}")


if __name__ == "__main__":
    main()

