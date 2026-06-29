-- Retail Profitability and Customer Retention Analytics
-- SQL dialect: PostgreSQL-style. Easy to adapt for MySQL, BigQuery, Snowflake, or SQL Server.

-- 1. Monthly KPI trend
SELECT
    DATE_TRUNC('month', o.order_date)::date AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT o.customer_id) AS active_customers,
    ROUND(SUM(o.quantity * o.unit_price_inr), 2) AS revenue_inr,
    ROUND(SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr), 2) AS gross_profit_inr,
    ROUND(
        SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr)
        / NULLIF(SUM(o.quantity * o.unit_price_inr), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN products p ON p.product_id = o.product_id
GROUP BY 1
ORDER BY 1;

-- 2. Region and country profitability
SELECT
    c.country,
    c.region,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.quantity * o.unit_price_inr), 2) AS revenue_inr,
    ROUND(SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr), 2) AS gross_profit_inr,
    ROUND(
        SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr)
        / NULLIF(SUM(o.quantity * o.unit_price_inr), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
GROUP BY c.country, c.region
ORDER BY gross_profit_inr DESC;

-- 3. Products with high revenue but weak margin
SELECT
    p.category,
    p.product_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.quantity * o.unit_price_inr), 2) AS revenue_inr,
    ROUND(SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr), 2) AS gross_profit_inr,
    ROUND(AVG(o.discount_pct), 2) AS avg_discount_pct
FROM orders o
JOIN products p ON p.product_id = o.product_id
GROUP BY p.category, p.product_name
HAVING SUM(o.quantity * o.unit_price_inr) > 500000
ORDER BY gross_profit_inr ASC;

-- 4. Customer repeat purchase rate by acquisition channel
WITH customer_orders AS (
    SELECT
        c.acquisition_channel,
        c.customer_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.acquisition_channel, c.customer_id
)
SELECT
    acquisition_channel,
    COUNT(*) AS customers,
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) AS repeat_rate_pct
FROM customer_orders
GROUP BY acquisition_channel
ORDER BY repeat_rate_pct DESC;

-- 5. Churn-risk customers inactive for 90+ days
WITH latest_order AS (
    SELECT MAX(order_date) AS max_order_date FROM orders
),
customer_last_order AS (
    SELECT
        c.customer_id,
        c.country,
        c.segment,
        MAX(o.order_date) AS last_order_date
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.country, c.segment
)
SELECT
    clo.customer_id,
    clo.country,
    clo.segment,
    clo.last_order_date,
    (lo.max_order_date - clo.last_order_date) AS inactive_days
FROM customer_last_order clo
CROSS JOIN latest_order lo
WHERE (lo.max_order_date - clo.last_order_date) >= 90
ORDER BY inactive_days DESC;

-- 6. Delivery SLA breach rate by country and segment
SELECT
    c.country,
    c.segment,
    COUNT(*) AS orders,
    SUM(CASE WHEN o.actual_delivery_date > o.promised_delivery_date THEN 1 ELSE 0 END) AS late_orders,
    ROUND(
        SUM(CASE WHEN o.actual_delivery_date > o.promised_delivery_date THEN 1 ELSE 0 END)::numeric
        / COUNT(*) * 100,
        2
    ) AS sla_breach_rate_pct
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.country, c.segment
ORDER BY sla_breach_rate_pct DESC;

-- 7. Discount bands and profitability
SELECT
    CASE
        WHEN o.discount_pct = 0 THEN '0%'
        WHEN o.discount_pct BETWEEN 1 AND 10 THEN '1-10%'
        WHEN o.discount_pct BETWEEN 11 AND 20 THEN '11-20%'
        ELSE '21%+'
    END AS discount_band,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.quantity * o.unit_price_inr), 2) AS revenue_inr,
    ROUND(SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr), 2) AS gross_profit_inr,
    ROUND(
        SUM(o.quantity * (o.unit_price_inr - p.unit_cost_inr) - o.delivery_cost_inr)
        / NULLIF(SUM(o.quantity * o.unit_price_inr), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN products p ON p.product_id = o.product_id
GROUP BY 1
ORDER BY gross_margin_pct DESC;

