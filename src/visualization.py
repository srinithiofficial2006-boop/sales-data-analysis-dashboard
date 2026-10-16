import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_sales_data.csv"
)

CHART_DIR = (
    BASE_DIR
    / "outputs"
    / "charts"
)

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"]
)


sns.set_theme(
    style="whitegrid"
)


# --------------------------------------------------
# 1. MONTHLY SALES
# --------------------------------------------------

monthly_sales = (
    df.groupby(
        df["Order_Date"]
        .dt.to_period("M")
    )["Sales"]
    .sum()
)

plt.figure(
    figsize=(12, 6)
)

monthly_sales.plot(
    marker="o"
)

plt.title(
    "Monthly Sales Trend"
)

plt.xlabel("Month")

plt.ylabel("Sales")

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "monthly_sales.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 2. SALES BY CATEGORY
# --------------------------------------------------

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(9, 6)
)

category_sales.plot(
    kind="bar"
)

plt.title(
    "Sales by Category"
)

plt.xlabel("Category")

plt.ylabel("Sales")

plt.xticks(
    rotation=30
)

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "category_sales.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 3. PROFIT BY CATEGORY
# --------------------------------------------------

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(9, 6)
)

category_profit.plot(
    kind="bar"
)

plt.title(
    "Profit by Category"
)

plt.xlabel("Category")

plt.ylabel("Profit")

plt.xticks(
    rotation=30
)

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "category_profit.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 4. SALES BY REGION
# --------------------------------------------------

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(9, 6)
)

region_sales.plot(
    kind="bar"
)

plt.title(
    "Sales by Region"
)

plt.xlabel("Region")

plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "region_sales.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 5. TOP 10 PRODUCTS
# --------------------------------------------------

top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .sort_values()
)

plt.figure(
    figsize=(10, 6)
)

top_products.plot(
    kind="barh"
)

plt.title(
    "Top 10 Products by Sales"
)

plt.xlabel("Sales")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "top_products.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 6. SALES VS PROFIT
# --------------------------------------------------

plt.figure(
    figsize=(10, 6)
)

sns.scatterplot(
    data=df,
    x="Sales",
    y="Profit",
    hue="Category"
)

plt.title(
    "Sales vs Profit"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR
    / "sales_vs_profit.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# COMPLETION
# --------------------------------------------------

print("=" * 60)
print("VISUALIZATION COMPLETED")
print("=" * 60)

print(
    f"\nCharts saved in:\n{CHART_DIR}"
)