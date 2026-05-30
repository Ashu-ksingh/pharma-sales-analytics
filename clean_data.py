import pandas as pd

# Load the data
df = pd.read_csv('salesmonthly.csv')

# 1. Rename datum to date
df.rename(columns={'datum': 'date'}, inplace=True)

# 2. Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# 3. Extract year and month as separate columns
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%b')

# 4. Round all sales columns to 2 decimal places
sales_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']
df[sales_cols] = df[sales_cols].round(2)

# 5. Add total sales column
df['total_sales'] = df[sales_cols].sum(axis=1).round(2)

# 6. Check result
print(df.head())
print(df.columns.tolist())

# 7. Save cleaned file
df.to_csv('salesmonthly_cleaned.csv', index=False)
print("Cleaned file saved successfully")

print(df.shape)
print(df[['date', 'year', 'month', 'month_name', 'total_sales']].head(10))