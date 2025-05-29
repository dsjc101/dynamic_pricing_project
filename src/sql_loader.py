import pandas as pd
import sqlite3
import os
# Path to cleaned CSV
csv_path = "data/Online_Retail_Clean.csv"
# Reading the data
df = pd.read_csv(csv_path)
# Creating output DB directory 
os.makedirs("data", exist_ok=True)
# Connecting to SQLite DB 
conn = sqlite3.connect("data/retail.db")
# Loading data into a new table
df.to_sql("transactions", conn, if_exists="replace", index=False)
# Closing the connection
conn.close()

