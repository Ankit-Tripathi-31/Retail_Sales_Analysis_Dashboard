# Retail Sales Business Analysis

## Executive summary

The cleaned dataset contains **1,000 unique orders** and reports **1,145,049.83 sales units**, **199,687.65 profit units**, and a **17.44% overall profit margin**. Technology generates the most sales by a wide margin. Performance is not uniform: Central has the weakest regional margin, while the 2025 margin is lower than 2024 even as the dataset records sales in both full calendar years.

Financial amounts are expressed in the dataset's units. A currency is not specified consistently enough in the source to label the totals as a particular currency.

## Scope and metric definitions

- **Input:** `Retail_Sales_Raw_Dataset.csv` (1,012 rows, 16 columns).
- **Analysis grain:** one row per `Order_ID`; the first occurrence of a repeated ID is retained.
- **Sales and profit:** sums of the source-reported `Sales_Amount` and `Profit` fields. They are not recalculated from unit price, cost, quantity, or discount.
- **Profit margin:** total profit divided by total sales for the same filtered group.
- **Average sales per order:** total sales divided by order count.
- **Trend coverage:** the date range is January 1, 2024 to December 30, 2025. Orders with a missing or unparseable date remain in the dataset but cannot appear in month- or year-based analyses.

## Overall performance

| Metric | Result |
|---|---:|
| Unique orders | 1,000 |
| Sales | 1,145,049.83 |
| Profit | 199,687.65 |
| Overall profit margin | 17.44% |
| Average sales per order | 1,145.05 |
| Orders with negative reported sales | 4 |
| Orders with negative reported profit | 149 |

## Findings

### Product mix

| Product category | Orders | Sales | Profit | Margin |
|---|---:|---:|---:|---:|
| Technology | 357 | 759,865.30 | 134,689.76 | 17.73% |
| Furniture | 282 | 350,946.05 | 58,884.81 | 16.78% |
| Office Supplies | 361 | 34,238.48 | 6,113.08 | 17.85% |

Technology contributes approximately **66.4% of sales** and **67.5% of profit**. Laptops alone account for 365,347.19 sales units, making them the largest individual product by sales. This concentration is useful for prioritization but also means that product availability and category mix deserve monitoring.

### Regional performance

| Region | Orders | Sales | Profit | Margin |
|---|---:|---:|---:|---:|
| North | 206 | 243,949.83 | 44,948.25 | 18.43% |
| East | 206 | 235,748.61 | 43,456.69 | 18.43% |
| Central | 193 | 230,284.39 | 29,916.16 | 12.99% |
| South | 194 | 222,491.28 | 38,840.08 | 17.46% |
| West | 201 | 212,575.72 | 42,526.47 | 20.01% |

North leads sales, while West has the highest regional margin. Central's margin is the lowest at **12.99%**, roughly 5.4 percentage points below the overall margin, despite its sales being close to other regions. Review Central's product mix, discounting, and costs before drawing conclusions about the cause.

### Sales channels

| Channel | Orders | Sales | Profit | Margin |
|---|---:|---:|---:|---:|
| Online | 345 | 390,936.01 | 65,500.89 | 16.75% |
| Phone | 322 | 385,577.24 | 60,527.57 | 15.70% |
| Retail Store | 333 | 368,536.58 | 73,659.19 | 19.99% |

Online has the highest sales, while Retail Store produces the highest profit and margin. The phone channel has the lowest margin. The dataset does not include channel operating costs, so channel profitability differences should be investigated rather than attributed to a specific cause.

### Year-over-year comparison

| Order year | Orders with usable dates | Sales | Profit | Margin |
|---|---:|---:|---:|---:|
| 2024 | 491 | 602,119.83 | 116,463.62 | 19.34% |
| 2025 | 500 | 539,241.39 | 83,073.27 | 15.41% |

Compared with 2024, 2025 reported sales decreased **10.44%**, profit decreased **28.67%**, and margin declined by **3.93 percentage points**. Both years have recorded orders across all twelve calendar months, but this is a two-year snapshot, not a forecast or a causal explanation.

## Recommended actions

1. **Investigate Central's margin:** compare discount rates, product mix, and unit costs with other regions before changing regional pricing or targets.
2. **Review the 2025 profit decline:** break down the year-over-year movement by month, product, region, and channel; validate the reported profit and sales fields first.
3. **Monitor product concentration:** track laptop and Technology availability alongside category profitability to understand the impact of changes in the sales mix.
4. **Compare channel economics:** investigate the lower Phone and Online margins using fulfillment, service, and promotional costs, which are not present in this dataset.
5. **Resolve data-quality exceptions:** validate duplicate order IDs, missing dates, and negative quantity/sales records with the source system before using the results for financial decisions.

## Data preparation and limitations

The companion `prepare_dashboard.py` script applies these rules:

1. Keep the first row for each `Order_ID`, removing 12 repeated rows. Three duplicated IDs have differences between their rows; the first-row rule is a deterministic choice, not proof that the retained row is correct.
2. Trim text, standardize category and label casing, and map blank or literal `null` categorical values to `Unknown`.
3. Parse supported ISO, month-first, day-first, and abbreviated-month date formats to `YYYY-MM-DD`. Month-first formats are attempted before day-first formats where both interpretations are possible. Blank or invalid dates remain blank.
4. Strip a leading `₹` and commas from unit-price/cost/sales/profit numeric values, then normalize valid monetary values to two decimal places. Quantity is kept as an integer.
5. Leave missing numeric values blank. Discounts outside the valid 0–1 range are blanked rather than assumed to be zero.
6. Preserve negative quantities, sales, and profits as supplied. Five orders have a negative quantity, while all five have positive reported sales; this is a reconciliation issue, not a basis for silently changing the data.

After cleaning, nine orders have no usable date; 26 cities, 12 customer segments, six payment methods, and 15 sales representatives are unknown. Eight unit costs and 15 discount values are blank (10 missing discounts and five invalid rates greater than 1). Unit price contains 14 values with a leading rupee symbol, but the dataset does not establish a consistent currency field.

The source-reported sales and profit values are retained because the source also contains missing costs/discounts and negative quantities alongside positive sales. Consequently, this analysis describes the supplied financial measures; it does not certify that the underlying transaction calculations reconcile.
