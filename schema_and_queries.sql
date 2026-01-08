CREATE DATABASE sales_analytics;
USE sales_analytics;

CREATE TABLE sales (
    product_id INT,
    sale_date DATE,
    sales_rep VARCHAR(50),
    region VARCHAR(50),
    sales_amount DECIMAL(10,2),
    quantity_sold INT,
    product_category VARCHAR(50),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    customer_type VARCHAR(20),
    discount DECIMAL(5,2),
    payment_method VARCHAR(30),
    sales_channel VARCHAR(30),
    region_and_sales_rep VARCHAR(100),
    year INT,
    month INT
);

SELECT COUNT(*) FROM sales;
SELECT * FROM sales LIMIT 5;

-- 1 Overall Sales Performance (KPI Query)
SELECT 
    COUNT(*) AS total_transactions,
    SUM(sales_amount) AS total_sales,
    SUM(quantity_sold) AS total_units_sold,
    AVG(sales_amount) AS avg_sales_per_transaction
FROM sales;

-- 2 Monthly Sales Trend
SELECT 
    year,
    month,
    ROUND(SUM(sales_amount), 2) AS monthly_sales
FROM sales
GROUP BY year, month
ORDER BY year, month;

-- 3 Region-wise Sales Performance
SELECT 
    region,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    SUM(quantity_sold) AS total_units
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- 4 Top Performing Sales Representatives
SELECT 
    sales_rep,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM sales
GROUP BY sales_rep
ORDER BY total_sales DESC
LIMIT 5;

-- 5 Product Category Analysis
SELECT 
    product_category,
    ROUND(SUM(sales_amount), 2) AS category_sales
FROM sales
GROUP BY product_category
ORDER BY category_sales DESC;

-- 6 Discount Impact Analysis
SELECT 
    discount,
    COUNT(*) AS transactions,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM sales
GROUP BY discount
ORDER BY discount;

-- 7 Sales Channel Performance
SELECT 
    sales_channel,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM sales
GROUP BY sales_channel;








