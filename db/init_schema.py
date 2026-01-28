"""
Initialize SQLite database schema
Run this ONCE to create tables
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/fraud_claims.db")
SCHEMA_PATH = Path("db/schema.sql")

# Ensure data folder exists
DB_PATH.parent.mkdir(exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Execute schema SQL
with open(SCHEMA_PATH, "r") as f: # Open and read the schema file
    schema_sql = f.read() # Read the SQL commands
    conn.executescript(schema_sql) # Execute the SQL script to create tables

conn.close() # Close the connection

print("Schema created successfully.")
