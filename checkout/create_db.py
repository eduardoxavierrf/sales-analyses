import sqlite3
import pandas as pd

checkout_1 = pd.read_csv('checkout_1.csv')
checkout_1['day'] = 1

checkout_2 = pd.read_csv('checkout_2.csv')
checkout_2['day'] = 2

checkout = pd.concat([checkout_1, checkout_2], ignore_index=True)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS checkout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    day INTEGER,
    today INTEGER,
    yesterday INTEGER,
    same_day_last_week INTEGER,
    avg_last_week REAL,
    avg_last_month REAL
);'''


cursor.execute(create_table_query)

checkout.to_sql('checkout', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("Data inserted successfully.")
