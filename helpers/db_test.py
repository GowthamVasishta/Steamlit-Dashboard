# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:21:03 2024

@author: gowth
"""

import sqlite3
import pandas as pd
import os

# Create a sample DataFrame
data = {
    "id": [7, 8, 9],
    "name": ["Grace", "Hank", "Ivy"],
    "age": [22, 29, 34]
}
df = pd.DataFrame(data)

# Define the drive and folder path where the database file should be saved
drive_path = "C:/Users/Documents"  # Adjust the path as needed
db_file_name = "example.db"
db_file = os.path.join(drive_path, db_file_name)

# Ensure the folder exists
os.makedirs(drive_path, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Insert the DataFrame into the SQLite table
table_name = "users"
df.to_sql(table_name, conn, if_exists='append', index=False)

# Close the database connection
conn.close()

print(f"Data appended and database saved to: {db_file}")



import sqlite3

# Define the database file path
db_file = "C:/Users/Documents/example.db"
table_name = "users"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Execute the SQL query to calculate the sum of the 'age' column
query = f"SELECT SUM(age) as total_age FROM {table_name}"
result = conn.execute(query).fetchone()

# Close the database connection
conn.close()

# Extract the sum from the result
age_sum = result[0] if result[0] is not None else 0

print(f"The sum of the 'age' column is: {age_sum}")
