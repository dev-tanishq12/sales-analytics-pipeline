import pandas as pd
import mysql.connector

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("sales_data.csv")

print("Initial Data Preview:")
print(df.head())
print("\nShape:", df.shape)
print("\nMissing values:\n", df.isnull().sum())

# =========================
# 2. DATA CLEANING
# =========================
df = df.drop_duplicates()

# Convert date
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'], dayfirst=True)

# Fill numerical columns
num_cols = df.select_dtypes(include='number').columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill categorical columns
cat_cols = df.select_dtypes(include='object').columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Feature engineering
df['Year'] = df['Sale_Date'].dt.year
df['Month'] = df['Sale_Date'].dt.month

# =========================
# 3. STANDARDIZE COLUMN NAMES
# =========================
df.columns = df.columns.str.lower().str.strip()

print("\nColumns after standardization:")
print(df.columns.tolist())

# =========================
# 4. CONNECT TO MYSQL
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qhsinat12sql*",
    database="sales_analytics",
    port=3306
)
cursor = conn.cursor()
print("\nConnected to MySQL successfully!")

# =========================
# 5. SELECT EXACT COLUMNS (MATCH TABLE)
# =========================
df = df[
    [
        'product_id',
        'sale_date',
        'sales_rep',
        'region',
        'sales_amount',
        'quantity_sold',
        'product_category',
        'unit_cost',
        'unit_price',
        'customer_type',
        'discount',
        'payment_method',
        'sales_channel',
        'region_and_sales_rep',
        'year',
        'month'
    ]
]

print("\nFinal DataFrame shape:", df.shape)
print(df.head())

# =========================
# 6. INSERT INTO MYSQL
# =========================
insert_query = """
INSERT INTO sales (
    product_id, sale_date, sales_rep, region, sales_amount,
    quantity_sold, product_category, unit_cost, unit_price,
    customer_type, discount, payment_method, sales_channel,
    region_and_sales_rep, year, month
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.to_numpy()]

cursor.executemany(insert_query, data)
conn.commit()

print(f"\n✅ Data inserted successfully: {len(data)} rows")

# =========================
# 7. CLOSE CONNECTION
# =========================
cursor.close()
conn.close()
print("Database connection closed.")
