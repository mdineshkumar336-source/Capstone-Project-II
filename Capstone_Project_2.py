
# Capstone Project - II

# MODULE 1 - Data Audit & Cleaning

# Load the Files

import pandas as pd
import numpy as np

customers = pd.read_csv("Capstone_Customers.csv")
orders = pd.read_csv("Capstone_Orders.csv")

print("Customers shape:", customers.shape)
print("Orders shape:", orders.shape)

# Shape & Data Types

print("\nCustomers Data Types:")
print(customers.dtypes)

print("\nOrders Data Types:")
print(orders.dtypes)

# Missing Value Audit

print("Missing values - Customers:")
print(customers.isna().sum())

print("\nMissing values - Orders:")
print(orders.isna().sum())

# Check Duplicates

print("Duplicate customer rows:", customers.duplicated().sum())
print("Duplicate order rows:", orders.duplicated().sum())

# Check Unique Values

print("========== CUSTOMERS TEXT VALUES ==========")

for col in customers.select_dtypes(include="object").columns:
    print("\n", col)
    print(customers[col].dropna().unique())


print("\n========== ORDERS TEXT VALUES ==========")

for col in orders.select_dtypes(include="object").columns:
    print("\n", col)
    print(orders[col].dropna().unique())
    
# Standardize Whitespace and Casing

# Text

def standardize_text(df):
    df = df.copy()

    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    return df


customers = standardize_text(customers)
orders = standardize_text(orders)

# ID's

customers["CustomerID"] = customers["CustomerID"].str.upper()

orders["CustomerID"] = orders["CustomerID"].str.upper()
orders["OrderID"] = orders["OrderID"].str.upper()

# Customer Categories

customers["Segment"] = customers["Segment"].str.title()
customers["Region"] = customers["Region"].str.title()
customers["City"] = customers["City"].str.title()
customers["State"] = customers["State"].str.title()

# Order Categories

orders["ProductCategory"] = orders["ProductCategory"].str.title()
orders["Product"] = orders["Product"].str.title()
orders["OrderStatus"] = orders["OrderStatus"].str.title()
orders["PaymentMethod"] = orders["PaymentMethod"].str.lower()

# Payment Names

orders["PaymentMethod"] = orders["PaymentMethod"].replace({
    "net banking": "NetBanking",
    "netbanking": "NetBanking",
    "upi": "UPI",
    "card": "Card",
    "cash on delivery": "Cash on Delivery"
})

# Check Orphan CustomerIDs

customer_ids = set(customers["CustomerID"])

orphan_orders = orders[
    ~orders["CustomerID"].isin(customer_ids)
]

print("Orphan orders:", len(orphan_orders))
print(orphan_orders["CustomerID"].unique())

# Handle Missing Values Individually

# Missing Segment

customers["Segment"] = customers["Segment"].fillna(
    customers["Segment"].mode()[0]
)

# Missing Region

customers["Region"] = customers["Region"].fillna(
    customers["Region"].mode()[0]
)

# Orders

orders = orders.dropna(
    subset=["ProductCategory", "Product"]
).copy()

# Payment Methods

orders["PaymentMethod"] = orders["PaymentMethod"].fillna("Unknown")

# Order Status

orders["OrderStatus"] = orders["OrderStatus"].fillna("Unknown")

# Quantity

orders = orders.dropna(
    subset=["Quantity"]
).copy()

# Discount

orders["Discount"] = orders["Discount"].fillna(0)

# Profit

orders = orders.dropna(
    subset=["Profit"]
).copy()

# Remove Orphan Orders

customer_ids = set(customers["CustomerID"])

orders = orders[
    orders["CustomerID"].isin(customer_ids)
].copy()

# Remove Duplicates

customers = customers.drop_duplicates().copy()
orders = orders.drop_duplicates().copy()

# Convert Tables

customers["SignupDate"] = pd.to_datetime(
    customers["SignupDate"],
    errors="coerce"
)

orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)

# Final Audit

print("========== FINAL AUDIT ==========")

print("\nCustomers shape:", customers.shape)
print("Orders shape:", orders.shape)

print("\nCustomer missing values:")
print(customers.isna().sum())

print("\nOrder missing values:")
print(orders.isna().sum())

print("\nCustomer duplicates:",
      customers.duplicated().sum())

print("Order duplicates:",
      orders.duplicated().sum())

# Data Cleaning Log

cleaning_log = pd.DataFrame({
    "Issue": [
        "Missing Segment",
        "Missing Region",
        "Missing Product/ProductCategory",
        "Missing PaymentMethod",
        "Missing OrderStatus",
        "Missing Quantity",
        "Missing Discount",
        "Missing Profit",
        "Duplicate customer row",
        "Duplicate order rows",
        "Orphan CustomerIDs",
        "Whitespace/casing inconsistencies"
    ],

    "Rows Affected": [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 5, 8, "Multiple"
    ],

    "Action": [
        "Filled with mode",
        "Filled with mode",
        "Removed order",
        "Filled with Unknown",
        "Filled with Unknown",
        "Removed order",
        "Filled with 0",
        "Removed order",
        "Removed duplicate",
        "Removed duplicates",
        "Removed unmatched orders",
        "Trimmed and standardized text"
    ],

    "Why": [
        "Categorical field; mode is appropriate for one missing value",
        "Categorical field; mode is appropriate for one missing value",
        "Product information cannot be safely inferred",
        "Payment method cannot be reliably inferred",
        "Status cannot be reliably inferred",
        "Required for quantity-based analysis",
        "Missing discount treated as no discount",
        "Profit should not be invented",
        "Exact duplicate record",
        "Exact duplicate records",
        "No matching customer exists",
        "Ensures consistent grouping and joining"
    ]
})

print(cleaning_log)

# Save it

cleaning_log.to_excel(
    "Data_Cleaning_Log.xlsx",
    index=False
)

# MODULE 2 - Python & NumPy Foundations

# Loading Function

def load_data(customer_file, order_file):
    try:
        customers = pd.read_csv(customer_file)
        orders = pd.read_csv(order_file)

        return customers, orders

    except FileNotFoundError as e:
        print("File not found:", e)
        raise

    except pd.errors.ParserError as e:
        print("CSV file is corrupted or incorrectly formatted:", e)
        raise

    except Exception as e:
        print("Unexpected error:", e)
        raise
    
    customers, orders = load_data(
    "Capstone_Customers.csv",
    "Capstone_Orders.csv"
)
    
# NumPy Calculations

sales_array = orders["Sales"].to_numpy()

print("Mean Sales:", np.mean(sales_array))
print("Standard Deviation:", np.std(sales_array))
print("Minimum Sales:", np.min(sales_array))
print("Maximum Sales:", np.max(sales_array))

# Normalization

sales_min = np.min(sales_array)
sales_max = np.max(sales_array)

sales_normalized = (
    (sales_array - sales_min) /
    (sales_max - sales_min)
)

print(sales_normalized[:10])

# Loss Flag

orders["Loss_Flag"] = np.where(
    orders["Profit"] < 0,
    "Loss",
    "Profit"
)

print(orders["Loss_Flag"].value_counts())

# MODULE 3 - Pandas Wrangling & EDA

# Merge

merged = orders.merge(
    customers,
    on="CustomerID",
    how="left",
    validate="many_to_one"
)

print("Merged shape:", merged.shape)

# Calculated Columns

# Profit Margin

merged["Profit Margin"] = np.where(
    merged["Sales"] != 0,
    merged["Profit"] / merged["Sales"] * 100,
    0
)

# Per Unit

merged["Profit per Unit"] = np.where(
    merged["Quantity"] != 0,
    merged["Profit"] / merged["Quantity"],
    0
)

# Group By

region_summary = merged.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Order_Count=("OrderID", "nunique"),
    Average_Order_Value=("Sales", "mean")
).sort_values(
    "Total_Sales",
    ascending=False
)

print(region_summary)

# Pivot Table

pivot_region_segment = pd.pivot_table(
    merged,
    values="Sales",
    index="Region",
    columns="Segment",
    aggfunc="sum",
    fill_value=0
)

print(pivot_region_segment)

# IQR Outlier Detection

def find_iqr_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    return outliers, lower, upper

sales_outliers, lower, upper = find_iqr_outliers(
    merged,
    "Sales"
)

print("Sales lower limit:", lower)
print("Sales upper limit:", upper)
print("Sales outliers:", len(sales_outliers))

# Correlation Matrix

corr = merged[
    ["Sales", "Profit", "Quantity", "Discount"]
].corr()

print(corr)

# Plain-English interpretation:

# Sales and Quantity have a strong positive relationship of 0.746. In this dataset, higher quantities are generally associated with higher sales.

# MODULE 4 - Statistics

# Descriptive Statistics

stats = merged[
    ["Sales", "Profit", "Quantity", "Discount"]
].describe()

print(stats)

# Two Random Samples

sample_1 = merged.sample(
    n=50,
    random_state=42
)

sample_2 = merged.sample(
    n=50,
    random_state=7
)

print("Full dataset mean:",
      merged["Sales"].mean())

print("Sample 1 mean:",
      sample_1["Sales"].mean())

print("Sample 2 mean:",
      sample_2["Sales"].mean())

# T-test

from scipy.stats import ttest_ind

east_profit = merged.loc[
    merged["Region"] == "East",
    "Profit"
]

west_profit = merged.loc[
    merged["Region"] == "West",
    "Profit"
]

t_stat, p_value = ttest_ind(
    east_profit,
    west_profit,
    equal_var=False
)

print("T-statistic:", t_stat)
print("P-value:", p_value)

# MODULE 5 - Visualization

# Import Matplotlib

import matplotlib.pyplot as plt

# Chart 1 - Region Comparison

region_sales = merged.groupby("Region")["Sales"].sum()

region_sales.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Insight

# South generated ₹77.22 million, contributing 53.61% of total sales.

# Chart 2 - Sales Trend

monthly_sales = merged.groupby(
    merged["OrderDate"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# insight:

# June 2026 recorded the highest monthly sales at ₹16.73 million.

# Chart 3 - Distribution

merged["Sales"].plot(kind="hist", bins=30)

plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Insight:

# Median Sales is ₹10,900, substantially below the ₹28,875.02 mean, indicating a right-skewed distribution.

# Chart 4 - Relationship

plt.scatter(
    merged["Quantity"],
    merged["Sales"]
)

plt.title("Sales vs Quantity")
plt.xlabel("Quantity")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# Insight:

# Sales and Quantity have a correlation of 0.746, showing a strong positive relationship.

# Chart 5 - Outlier View

plt.boxplot(merged["Sales"])

plt.title("Sales Outlier Detection")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# Insight:

# 392 Sales records are above the IQR upper limit of ₹76,950, with the maximum transaction reaching ₹6.19 million.

# Chart 6 - Correlation Heatmap

import matplotlib.pyplot as plt

corr = merged[
    ["Sales", "Profit", "Quantity", "Discount"]
].corr()

plt.imshow(corr, interpolation="nearest")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# Insight:

# Sales and Quantity show the strongest relationship at 0.746, while no other variable pair crosses ±0.30.

# Module 6 - Excel Reporting

import os
import pandas as pd

os.makedirs("outputs", exist_ok=True)

excel_file = "outputs/analytics_report.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    customers.to_excel(
        writer,
        sheet_name="Cleaned_Customers",
        index=False
    )

    orders.to_excel(
        writer,
        sheet_name="Cleaned_Orders",
        index=False
    )

    merged.to_excel(
        writer,
        sheet_name="Merged_Data",
        index=False
    )

    cleaning_log.to_excel(
        writer,
        sheet_name="Cleaning_Log",
        index=False
    )

print("\nExcel export completed successfully.")
print("File:", excel_file)

# Import Cleaned CSV File

customers.to_csv(
    "outputs/Cleaned_Customers.csv",
    index=False
)

orders.to_csv(
    "outputs/Cleaned_Orders.csv",
    index=False
)

# Module 9 - Customer Segmentation

import pandas as pd
import numpy as np

customers = pd.read_csv("Capstone_Customers.csv")
orders = pd.read_csv("Capstone_Orders.csv")

print(customers.shape)
print(orders.shape)

# Create Customer Level Features

customer_features = orders.groupby("CustomerID").agg(
    Total_Sales=("Sales", "sum"),
    Order_Count=("OrderID", "nunique")
).reset_index()

print(customer_features.head())

# Calculate Average Order Value

customer_features["Average_Order_Value"] = (
    customer_features["Total_Sales"]
    / customer_features["Order_Count"]
)

print(customer_features.head())

# Check Problems 

print(customer_features.isnull().sum())
print(customer_features.describe())

# Features for Clustering

X = customer_features[
    [
        "Total_Sales",
        "Order_Count",
        "Average_Order_Value"
    ]
]

print(X.head())

# Scale the Features

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print(X_scaled[:5])

# Elbow Method

from sklearn.cluster import KMeans

inertia = []

for k in range(2, 11):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    
    kmeans.fit(X_scaled)
    
    inertia.append(kmeans.inertia_)
    
# Plot of Elbow

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.plot(
    range(2, 11),
    inertia,
    marker="o"
)

plt.title("Elbow Method for Customer Segmentation")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")

plt.xticks(range(2, 11))
plt.grid(True)

plt.show()

# Run K-Means

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

customer_features["Cluster"] = kmeans.fit_predict(X_scaled)

print(customer_features.head())

# Analyze Each Cluster

cluster_summary = customer_features.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Average_Sales=("Total_Sales", "mean"),
    Average_Orders=("Order_Count", "mean"),
    Average_Order_Value=("Average_Order_Value", "mean")
).reset_index()

print(cluster_summary)

# Name the Clusters

cluster_names = {
    0: "Low-Value Customers",
    1: "Regular Customers",
    2: "High-Value Customers",
    3: "Premium Customers"
}

customer_features["Cluster_Name"] = (
    customer_features["Cluster"].map(cluster_names)
)

print(
    customer_features[
        [
            "CustomerID",
            "Total_Sales",
            "Order_Count",
            "Average_Order_Value",
            "Cluster",
            "Cluster_Name"
        ]
    ].head(10).to_string(index=False)
)

# Recommendation for Each Customer Cluster

cluster_recommendations = {
    "Low-Value Customers":
        "Run targeted promotions to increase purchase frequency and spending.",

    "Regular Customers":
        "Use loyalty rewards and personalized offers to increase order frequency.",

    "High-Value Customers":
        "Use personalized recommendations and upselling to increase customer value.",

    "Premium Customers":
        "Prioritize retention with exclusive offers and VIP benefits."
}

customer_features["Recommendation"] = (
    customer_features["Cluster_Name"]
    .map(cluster_recommendations)
)

recommendation_summary = (
    customer_features[
        ["Cluster", "Cluster_Name", "Recommendation"]
    ]
    .drop_duplicates()
    .sort_values("Cluster")
)

print(recommendation_summary.to_string(index=False))

# Save Customer Segmentation

customer_features.to_csv(
    "customer_segmentation.csv",
    index=False
)

recommendation_summary.to_csv(
    "cluster_recommendations.csv",
    index=False
)

print("\nFinal segmentation files saved successfully.")

# Save Cluster Summary

summary_file = "cluster_summary.csv"

cluster_summary.to_csv(
    summary_file,
    index=False
)

print(f"Cluster summary saved successfully:")
print(summary_file)

# Module 10 - KPI Reporting

# Load Cleaned Data

import pandas as pd

customers = pd.read_csv("Capstone_Customers.csv")
orders = pd.read_csv("Capstone_Orders.csv")

# KPI 1 - Total Sales

total_sales = orders["Sales"].sum()

print("KPI 1 - Total Sales")
print(f"Total Sales: ₹{total_sales:,.2f}") 

# Helps management evaluate overall revenue performance and set future sales targets.

# KPI 2 - Total Profit

total_profit = orders["Profit"].sum()

print("\nKPI 2 - Total Profit")
print(f"Total Profit: ₹{total_profit:,.2f}")

# Helps determine whether sales are generating sufficient profit and whether costs or pricing need attention.

# KPI 3 - Profit Margin %

profit_margin = (
    total_profit / total_sales
    if total_sales != 0
    else 0
)

print("\nKPI 3 - Profit Margin")
print(f"Profit Margin: {profit_margin:.2%}")

# Helps evaluate profitability relative to revenue and supports pricing and cost-control decisions.

# KPI 4 - Order Count

order_count = orders["OrderID"].nunique()

print("\nKPI 4 - Order Count")
print(f"Order Count: {order_count:,}")

# Helps monitor order volume and plan inventory, staffing, and operational capacity.

# KPI 5: Average Order Value

average_order_value = (
    total_sales / order_count
    if order_count != 0
    else 0
)

print("\nKPI 5 - Average Order Value")
print(f"Average Order Value: ₹{average_order_value:,.2f}")

# Helps identify opportunities to increase the amount customers spend per order through bundles, upselling, and cross-selling.

# KPI 6 - Customer Retention Rate

# First calculate orders per customer

orders_per_customer = (
    orders.groupby("CustomerID")["OrderID"]
    .nunique()
)

# Then

total_customers = orders_per_customer.shape[0]

retained_customers = (
    orders_per_customer > 1
).sum()

# Calculate the rate

retention_rate = (
    retained_customers / total_customers
    if total_customers != 0
    else 0
)

print("\nKPI 6 - Customer Retention Rate")
print(f"Retention Rate: {retention_rate:.2%}")

# Helps determine whether customers return and whether retention or loyalty programs need improvement.

# Create a KPIs Table

kpi_report = pd.DataFrame({
    "KPI": [
        "Total Sales",
        "Total Profit",
        "Profit Margin %",
        "Order Count",
        "Average Order Value",
        "Customer Retention Rate"
    ],

    "Value": [
        total_sales,
        total_profit,
        profit_margin,
        order_count,
        average_order_value,
        retention_rate
    ],

    "Used By": [
        "Sales Manager / Senior Management",
        "Senior Management / Finance Team",
        "Finance Manager / Senior Management",
        "Operations Manager / Sales Manager",
        "Sales Manager / Marketing Team",
        "Marketing Manager / Customer Success Team"
    ],

    "Business Decision": [
        "Evaluate revenue performance and set sales targets.",
        "Evaluate overall profitability and cost performance.",
        "Support pricing and cost-control decisions.",
        "Plan inventory, staffing, and operational capacity.",
        "Increase customer spending through upselling and cross-selling.",
        "Improve customer retention and loyalty strategies."
    ]
})

print("\nKPI Report Table:")
print(kpi_report.to_string(index=False))

# Best and Worst KPIs Explain

# Best KPI

best_kpi = {
    "KPI": "Customer Retention Rate",
    "Value": retention_rate,
    "Reason": (
        "The retention rate of 97.36% indicates that the business "
        "has a very strong repeat-customer base. This suggests "
        "customers are returning for additional purchases, which "
        "supports customer loyalty and reduces dependence on "
        "acquiring new customers."
    )
}

print(f"KPI    : {best_kpi['KPI']}")
print(f"Value  : {best_kpi['Value']:.2%}")
print(f"Why    : {best_kpi['Reason']}")

# Worst KPI

worst_kpi = {
    "KPI": "Profit Margin",
    "Value": profit_margin,
    "Reason": (
        "The profit margin of 8.44% indicates that only a relatively "
        "small portion of sales is converted into profit. Although "
        "the business may generate strong revenue, profitability "
        "could be improved by reviewing pricing, discounts, and costs."
    )
}

print(f"KPI    : {worst_kpi['KPI']}")
print(f"Value  : {worst_kpi['Value']:.2%}")
print(f"Why    : {worst_kpi['Reason']}")

# Save

kpi_report.to_csv(
    "module10_kpi_report.csv",
    index=False
)

print("\nKPI report saved successfully.")

