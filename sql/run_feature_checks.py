import sqlite3
import pandas as pd

conn = sqlite3.connect("data/fraud_claims.db")

print("Claim features sample:")
print(pd.read_sql(open("sql/claim_features.sql").read(), conn).head())

print("\nProvider features sample:")
print(pd.read_sql(open("sql/provider_features.sql").read(), conn).head())

print("\nMember features sample:")
print(pd.read_sql(open("sql/member_features.sql").read(), conn).head())

conn.close()
