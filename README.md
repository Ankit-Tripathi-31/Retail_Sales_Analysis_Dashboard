# Retail Sales Analysis Dashboard

🚀 **[View Live Dashboard](https://ankit-tripathi-31.github.io/Retail_Sales_Analysis_Dashboard/dashboard.html)**

An interactive retail sales dashboard built using HTML, CSS, and JavaScript.

---

## Get started

1. Open `dashboard.html` in a current desktop or mobile browser. It works directly from disk and does not require a web server, internet access, or third-party packages.
2. Use the region, category, segment, channel, and date filters to update the KPIs and charts.
3. Use **Night mode** to switch between light and dark themes.
4. Use **Download filtered CSV** to export the currently selected orders.

To regenerate the cleaned CSV and standalone dashboard after changing the source CSV, run:

```powershell
python prepare_dashboard.py
```

The script uses only the Python standard library. It reads the raw CSV from the project folder and writes `cleaned_retail_sales.csv` and `dashboard.html`. `dashboard_template.html` is the dashboard source template; the generated HTML embeds the cleaned data so it can be opened locally.

## Project files

| File                           | Purpose                                                |
| ------------------------------ | ------------------------------------------------------ |
| `Retail_Sales_Raw_Dataset.csv` | Original input dataset; left unchanged                 |
| `cleaned_retail_sales.csv`     | Deduplicated and normalized data used by the dashboard |
| `dashboard.html`               | Interactive dashboard with embedded cleaned data       |
| `dashboard_template.html`      | Source template for the generated dashboard            |
| `prepare_dashboard.py`         | Reproducible cleaning and dashboard-generation script  |
| `business_analysis.md`         | Methodology, results, caveats, and recommendations     |
| `insights.md`                  | Executive summary of the key findings                  |

## Data notes

The output contains 1,000 unique order IDs after removing 12 repeated IDs from 1,012 input rows. The cleaner normalizes text casing and whitespace, parses supported date formats to ISO dates, removes a leading rupee symbol from unit prices, and writes monetary values to two decimal places. Missing categorical values are labeled `Unknown`; missing or invalid dates, costs, and discounts remain blank. Discounts outside the 0–1 range are treated as invalid and left blank.

The cleaning rules and their impact are described in [business_analysis.md](./business_analysis.md). In particular, dates that cannot be parsed, duplicate IDs with conflicting row values, and negative quantities or sales should be reviewed before using the results for financial reporting. The source does not define a currency for all monetary fields, so dashboard amounts are shown without a currency symbol.

## Dashboard behavior

All metrics and charts update in the browser as filters change. Monthly trends omit orders without a usable date; other charts and totals include those orders unless a date filter is active. The dashboard calculates aggregates from the source-reported `Sales_Amount` and `Profit` fields rather than recalculating them from unit price, cost, quantity, and discount.
