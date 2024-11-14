import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("data.csv", encoding='ISO-8859-1')

# Remove rows with any null values
df_cleaned = df.dropna()

# Remove duplicate rows based on 'StockCode' and 'Description' columns
df_cleaned = df_cleaned.drop_duplicates(subset=["StockCode", "Description"])

# Ensure correct data types for 'UnitPrice' and 'Quantity'
df_cleaned['UnitPrice'] = pd.to_numeric(df_cleaned['UnitPrice'], errors='coerce')
df_cleaned['Quantity'] = pd.to_numeric(df_cleaned['Quantity'], errors='coerce')

# Save cleaned data to a JSON file
df_cleaned.to_json("products.json", orient="records")
