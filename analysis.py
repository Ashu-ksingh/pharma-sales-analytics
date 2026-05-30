import pandas as pd
import sqlite3

# Load cleaned data
df = pd.read_csv('salesmonthly_cleaned.csv')

# Create in-memory SQLite database
conn = sqlite3.connect(':memory:')
df.to_sql('pharma_sales', conn, index=False, if_exists='replace')

# Query 1 — Total sales by year
print("=== Total Sales by Year ===")
q1 = pd.read_sql_query("""
    SELECT year, 
           ROUND(SUM(total_sales), 2) AS yearly_sales
    FROM pharma_sales
    GROUP BY year
    ORDER BY year
""", conn)
print(q1)

# Query 2 — Best performing drug category overall
print("\n=== Best Performing Drug Category ===")
q2 = pd.read_sql_query("""
    SELECT 
        'M01AB' AS category, ROUND(SUM(M01AB), 2) AS total_sales FROM pharma_sales
    UNION ALL
    SELECT 'M01AE', ROUND(SUM(M01AE), 2) FROM pharma_sales
    UNION ALL
    SELECT 'N02BA', ROUND(SUM(N02BA), 2) FROM pharma_sales
    UNION ALL
    SELECT 'N02BE', ROUND(SUM(N02BE), 2) FROM pharma_sales
    UNION ALL
    SELECT 'N05B', ROUND(SUM(N05B), 2) FROM pharma_sales
    UNION ALL
    SELECT 'N05C', ROUND(SUM(N05C), 2) FROM pharma_sales
    UNION ALL
    SELECT 'R03', ROUND(SUM(R03), 2) FROM pharma_sales
    UNION ALL
    SELECT 'R06', ROUND(SUM(R06), 2) FROM pharma_sales
    ORDER BY total_sales DESC
""", conn)
print(q2)

# Query 3 — Month with highest sales each year
print("\n=== Best Month Per Year ===")
q3 = pd.read_sql_query("""
    SELECT year, month_name, total_sales
    FROM pharma_sales
    WHERE (year, total_sales) IN (
        SELECT year, MAX(total_sales)
        FROM pharma_sales
        GROUP BY year
    )
    ORDER BY year
""", conn)
print(q3)

# Query 4 — Year over year growth
print("\n=== Year Over Year Growth ===")
q4 = pd.read_sql_query("""
    SELECT year,
           ROUND(SUM(total_sales), 2) AS yearly_sales,
           ROUND(SUM(total_sales) - LAG(SUM(total_sales)) 
                 OVER (ORDER BY year), 2) AS growth
    FROM pharma_sales
    GROUP BY year
    ORDER BY year
""", conn)
print(q4)

# Save results for Power BI
q1.to_csv('yearly_sales.csv', index=False)
q2.to_csv('category_sales.csv', index=False)
q3.to_csv('best_month.csv', index=False)
q4.to_csv('yoy_growth.csv', index=False)
print("\nAll analysis files saved successfully")

conn.close()