import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_sales_data.csv"
)




def load_data():

    df = pd.read_csv(DATA_FILE)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"]
    )

    return df




def perform_analysis():

    df = load_data()

    print("\n")
    print("=" * 60)
    print("SALES PERFORMANCE ANALYSIS")
    print("=" * 60)

  

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order_ID"].nunique()

    total_quantity = df["Quantity"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales > 0
        else 0
    )

    print("\nKEY PERFORMANCE INDICATORS")

    print(
        f"Total Sales       : ₹{total_sales:,.2f}"
    )

    print(
        f"Total Profit      : ₹{total_profit:,.2f}"
    )

    print(
        f"Total Orders      : {total_orders}"
    )

    print(
        f"Total Quantity    : {total_quantity}"
    )

    print(
        f"Average Order     : ₹{average_order_value:,.2f}"
    )

    print(
        f"Profit Margin     : {profit_margin:.2f}%"
    )

   

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print("\n")
    print("SALES BY CATEGORY")
    print(category_sales)

    

    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print("\n")
    print("PROFIT BY CATEGORY")
    print(category_profit)



    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print("\n")
    print("SALES BY REGION")
    print(region_sales)


    state_sales = (
        df.groupby("State")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print("\n")
    print("TOP STATES BY SALES")
    print(state_sales.head(10))

    

    top_products = (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print("\n")
    print("TOP 10 PRODUCTS")
    print(top_products)

    

    monthly_sales = (
        df.groupby(
            df["Order_Date"]
            .dt.to_period("M")
        )["Sales"]
        .sum()
    )

    print("\n")
    print("MONTHLY SALES")
    print(monthly_sales)

    

    payment_analysis = (
        df["Payment_Method"]
        .value_counts()
    )

    print("\n")
    print("PAYMENT METHOD USAGE")
    print(payment_analysis)

   

    top_customers = (
        df.groupby(
            ["Customer_ID", "Customer_Name"]
        )["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print("\n")
    print("TOP 10 CUSTOMERS")
    print(top_customers)

    

    best_category = category_sales.idxmax()

    best_region = region_sales.idxmax()

    best_product = top_products.idxmax()

    print("\n")
    print("=" * 60)
    print("BUSINESS INSIGHTS")
    print("=" * 60)

    print(
        f"\nHighest Sales Category : {best_category}"
    )

    print(
        f"Highest Sales Region   : {best_region}"
    )

    print(
        f"Top Product            : {best_product}"
    )

    print("\nAnalysis completed successfully.")



if __name__ == "__main__":

    perform_analysis()