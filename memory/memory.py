import psycopg2
import numpy as np

# Connect to your database
conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost"
)
# Create a table with a vector column
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE test_items (
            id serial PRIMARY KEY,
            embedding vector(3)
        );
    """)
    conn.commit()
