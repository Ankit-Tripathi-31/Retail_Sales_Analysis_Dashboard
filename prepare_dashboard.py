import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Retail_Sales_Raw_Dataset.csv"
CLEANED = ROOT / "cleaned_retail_sales.csv"
TEMPLATE = ROOT / "dashboard_template.html"
DASHBOARD = ROOT / "dashboard.html"

DATE_FORMATS = (
    "%Y-%m-%d",
    "%m-%d-%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d-%b-%Y",
)
TEXT_FIELDS = (
    "Region",
    "City",
    "Customer_Segment",
    "Sales_Channel",
    "Product_Category",
    "Product_Name",
    "Payment_Method",
    "Sales_Rep",
)
MONEY_FIELDS = ("Unit_Price", "Unit_Cost", "Sales_Amount", "Profit")


def clean_date(value):
    value = value.strip()
    if not value:
        return ""
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).date().isoformat()
        except ValueError:
            continue
    return ""


def clean_text(value):
    value = value.strip()
    if not value or value.lower() == "null":
        return "Unknown"
    if value.upper() == "UPI":
        return "UPI"
    return value.title()


def clean_row(row):
    cleaned = {key: value.strip() for key, value in row.items()}
    cleaned["Order_Date"] = clean_date(cleaned["Order_Date"])
    for field in TEXT_FIELDS:
        cleaned[field] = clean_text(cleaned[field])

    for field in MONEY_FIELDS:
        value = cleaned[field].replace("₹", "").replace(",", "").strip()
        cleaned[field] = value
        if value:
            cleaned[field] = f"{float(value):.2f}"

    cleaned["Quantity"] = str(int(float(cleaned["Quantity"])))
    discount = cleaned["Discount_Rate"]
    if discount:
        rate = float(discount)
        cleaned["Discount_Rate"] = f"{rate:.2f}" if 0 <= rate <= 1 else ""
    return cleaned


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Dataset not found: {SOURCE}")
    if not TEMPLATE.is_file():
        raise FileNotFoundError(f"Dashboard template not found: {TEMPLATE}")

    with SOURCE.open(newline="", encoding="utf-8-sig") as source_file:
        reader = csv.DictReader(source_file)
        fields = reader.fieldnames
        if not fields:
            raise ValueError("The source CSV has no header row.")
        unique_rows = {}
        duplicate_count = 0
        for row in reader:
            order_id = row["Order_ID"].strip()
            if order_id in unique_rows:
                duplicate_count += 1
                continue
            unique_rows[order_id] = clean_row(row)

    rows = list(unique_rows.values())
    with CLEANED.open("w", newline="", encoding="utf-8") as cleaned_file:
        writer = csv.DictWriter(cleaned_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    embedded_data = json.dumps(rows, separators=(",", ":"), ensure_ascii=False)
    embedded_data = embedded_data.replace("<", "\\u003c")
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count("__DATA_JSON__") != 1:
        raise ValueError("Dashboard template must contain exactly one __DATA_JSON__ marker.")
    DASHBOARD.write_text(
        template.replace("__DATA_JSON__", embedded_data),
        encoding="utf-8",
    )

    print(f"Raw rows: {len(rows) + duplicate_count}")
    print(f"Duplicate order rows removed: {duplicate_count}")
    print(f"Cleaned rows: {len(rows)}")
    print(f"Cleaned dataset: {CLEANED.name}")
    print(f"Standalone dashboard: {DASHBOARD.name}")


if __name__ == "__main__":
    main()
