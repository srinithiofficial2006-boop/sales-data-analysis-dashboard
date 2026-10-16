import pandas as pd
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "sales_data.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "cleaned_sales_data.csv"



def clean_sales_data():

    print("=" * 60)
    print("SALES DATA CLEANING")
    print("=" * 60)

    
    print("\n1. Loading dataset...")

    df = pd.read_csv(RAW_FILE)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    

    print("\n2. Checking missing values...")

    missing = df.isnull().sum()

    print(missing[missing > 0])

    
    print("\n3. Checking duplicate records...")

    duplicates = df.duplicated().sum()

    print(f"Duplicate records: {duplicates}")

   
    df = df.drop_duplicates()

    

    print("\n4. Converting Order_Date...")

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Order_Date"]
    )

  
    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Discount",
        "Sales",
        "Cost",
        "Profit"
    ]

    print("\n5. Converting numeric columns...")

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    print("\n6. Handling missing numeric values...")

    for column in numeric_columns:

        df[column] = df[column].fillna(0)

    

    print("\n7. Handling missing categorical values...")

    categorical_columns = [
        "Customer_Name",
        "Product",
        "Category",
        "Sub_Category",
        "Region",
        "State",
        "Payment_Method"
    ]

    for column in categorical_columns:

        df[column] = df[column].fillna("Unknown")

    

    print("\n8. Removing invalid records...")

    df = df[df["Quantity"] > 0]

    df = df[df["Unit_Price"] >= 0]

    df = df[df["Sales"] >= 0]

    df = df[df["Cost"] >= 0]


    print("\n9. Calculating profit...")

    df["Profit"] = (
        df["Sales"] - df["Cost"]
    ).round(2)

    

    print("\n10. Creating derived columns...")

    df["Year"] = df["Order_Date"].dt.year

    df["Month"] = df["Order_Date"].dt.month

    df["Month_Name"] = (
        df["Order_Date"]
        .dt.strftime("%B")
    )

    df["Profit_Margin"] = 0.0

    valid_sales = df["Sales"] > 0

    df.loc[valid_sales, "Profit_Margin"] = (
        df.loc[valid_sales, "Profit"]
        / df.loc[valid_sales, "Sales"]
        * 100
    )

    df["Profit_Margin"] = (
        df["Profit_Margin"]
        .round(2)
    )

    

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_FILE,
        index=False
    )


    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)

    print(f"\nFinal rows    : {df.shape[0]}")
    print(f"Final columns : {df.shape[1]}")

    print(
        f"\nCleaned dataset saved to:\n"
        f"{PROCESSED_FILE}"
    )

    return df



if __name__ == "__main__":

    clean_sales_data()