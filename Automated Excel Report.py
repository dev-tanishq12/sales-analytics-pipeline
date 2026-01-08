import pandas as pd
import mysql.connector

# -------------------------
# 1. Connect to MySQL
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qhsinat12sql*",
    database="sales_analytics",
    port=3306
)

# -------------------------
# 2. SQL Queries
# -------------------------
summary_query = """
SELECT 
    COUNT(*) AS total_transactions,
    SUM(sales_amount) AS total_sales,
    SUM(quantity_sold) AS total_units
FROM sales;
"""

region_query = """
SELECT 
    region,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
"""

monthly_query = """
SELECT 
    year,
    month,
    ROUND(SUM(sales_amount), 2) AS monthly_sales
FROM sales
GROUP BY year, month
ORDER BY year, month;
"""

channel_query = """
SELECT 
    sales_channel,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM sales
GROUP BY sales_channel;
"""

# -------------------------
# 3. Load into DataFrames
# -------------------------
df_summary = pd.read_sql(summary_query, conn)
df_region = pd.read_sql(region_query, conn)
df_monthly = pd.read_sql(monthly_query, conn)
df_channel = pd.read_sql(channel_query, conn)

# -------------------------
# 4. Write to Excel
# -------------------------
with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Summary", index=False)
    df_region.to_excel(writer, sheet_name="Region_Sales", index=False)
    df_monthly.to_excel(writer, sheet_name="Monthly_Trend", index=False)
    df_channel.to_excel(writer, sheet_name="Sales_Channel", index=False)

conn.close()

print("✅ Automated Excel report generated: sales_report.xlsx")
