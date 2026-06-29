# Business-Project# Retail Profitability and Customer Retention Analytics

Portfolio project for Business Analyst, Data Analyst, BI Analyst, and Product Analyst roles in India and Canada.

## Business Problem

A mid-market omnichannel retailer is growing revenue but losing margin because of discounts, delivery costs, and repeat-customer decline. Leadership wants to know:

- Which customer segments and regions drive profitable growth?
- Which products sell well but damage margin?
- Which customers are at risk of churn?
- Where should the company reduce discounts or improve delivery operations?

## Why This Project Helps In Interviews

This project demonstrates job-ready business analytics skills:

- SQL for KPI reporting, segmentation, cohort analysis, and ranking
- Python for data cleaning, feature engineering, and exploratory analysis
- Dashboard design for executive decision-making
- Business storytelling with recommendations and trade-offs
- Metrics used in India and Canada analytics roles: revenue, gross margin, AOV, CAC proxy, repeat rate, churn risk, delivery SLA, regional performance

## Dataset

The project uses a generated synthetic retail dataset with realistic fields:

- `orders.csv`: order-level transactions
- `customers.csv`: customer demographics, region, acquisition channel
- `products.csv`: product category, cost, selling price, supplier country
- `monthly_kpis.csv`: monthly KPI summary generated from the analysis script

Run:

```bash
python3 src/generate_and_analyze.py
```

## Key Metrics

- Revenue = quantity * unit price after discount
- Gross profit = revenue - cost of goods sold - delivery cost
- Gross margin % = gross profit / revenue
- Average order value = revenue / orders
- Repeat customer rate = customers with 2+ orders / active customers
- Churn risk = customer inactive for 90+ days from latest order date
- Delivery SLA breach = delivered after promised date

## Suggested Dashboard Pages

1. Executive Overview
2. Profitability by Region and Category
3. Customer Retention and Churn Risk
4. Discount and Delivery Cost Diagnostics
5. Action Plan

Detailed dashboard requirements are in `dashboard/dashboard_spec.md`.

## Recommended Tools

Use any one stack:

- Power BI + SQL + Excel
- Tableau + SQL + Python
- Looker Studio + BigQuery/Sheets
- Python notebook + Streamlit

For India and Canada roles, Power BI + SQL is especially practical, while Python adds extra credibility.

## Project Story

The analysis finds that revenue growth alone is misleading. Some categories and regions produce high sales but low profit because of discounting and delivery costs. The business should shift from blanket discounts to targeted retention offers, improve delivery performance in high-breach regions, and prioritize profitable repeat customers.

## Portfolio Positioning

Use this title on LinkedIn/GitHub:

**Retail Profitability and Customer Retention Analytics | SQL, Python, Power BI**

Use this one-line description:

Built an end-to-end retail analytics project to identify margin leakage, churn risk, discount inefficiency, and regional growth opportunities using SQL, Python, and dashboard-ready KPIs.

