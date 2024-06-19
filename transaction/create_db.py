import sqlite3
import pandas as pd

transactions_1 = pd.read_csv('transactions_1.csv')
transactions_1['day'] = 1

transactions_2 = pd.read_csv('transactions_2.csv')
transactions_2['day'] = 2

transactions = pd.concat([transactions_1, transactions_2], ignore_index=True)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    status TEXT,
    count INTEGER,
    day INTEGER
);'''


cursor.execute(create_table_query)

transactions.to_sql('transactions', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("Data inserted successfully.")
