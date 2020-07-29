# module2-sql-for-analysis\assignment\elephant_assignment.py

import json
import psycopg2
from psycopg2.extras import DictCursor, execute_values
from dotenv import load_dotenv
import os
import pandas as pd


# > loads contents of the .env file into the script's environment
load_dotenv()


DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")


connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                              password=DB_PASSWORD, host=DB_HOST)

cursor = connection.cursor(cursor_factory=DictCursor)
print("CURSOR", type(cursor))

cursor.execute("SELECT * FROM test_table;")

result = cursor.fetchall()
for row in result:
    print("----")
    print(type(row))
    print(row)


# ---------------------------------------------------------


print("-------------------")
query = "SELECT usename, usecreatedb, usesuper, passwd FROM pg_user;"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall()[0:10]:
    print(row)


#
# CREATE THE TABLE
#

table_name = "test_table2"

# print("-------------------")
# query = f"""
# CREATE TABLE IF NOT EXISTS {table_name} (
#   id SERIAL PRIMARY KEY,
#   name varchar(40) NOT NULL,
#   data JSONB
# );
# """
# print("SQL:", query)
# cursor.execute(query)

#
# INSERT SOME DATA
#
my_dict = {"a": 1, "b": ["dog", "cat", 42], "c": 'true'}

# insertion_query = f"INSERT INTO {table_name} (name, data) VALUES (%s, %s)"
# cursor.execute(insertion_query, ('A rowwwww', 'null'))
# cursor.execute(insertion_query, ('Another row, with JSONNNNN', json.dumps
# (my_dict)))


# h/t: https://stackoverflow.com/questions/8134602/
# psycopg2-insert-multiple-rows-with-one-query
insertion_query = f"INSERT INTO {table_name} (name, data) VALUES %s"
execute_values(cursor, insertion_query, [
 ('A rowwwww', 'null'),
 ('Another row, with JSONNNNN', json.dumps(my_dict)),
 ('Third row', "3")
])  # The third param (data to be inserted) is a LIST of TUPLES


df = pd.DataFrame([
  ['A rowwwww', 'null'],
  ['Another row, with JSONNNNN', json.dumps(my_dict)],
  ['Third row', "null"],
  ["Pandas Row", "null"]
])
#  Convert df to a list of tuples

records = df.to_dict("records")  # > [{0: 'A rowwwww', 1: 'null'}, {0: 'Another
# row, with JSONNNNN', 1: '{"a": 1, "b": ["dog", "cat", 42], "c": "true"}'},
# {0: 'Third row', 1: '3'}, {0: 'Pandas Row', 1: 'YOOO!'}]
list_of_tuples = [(r[0], r[1]) for r in records]

execute_values(cursor, insertion_query, list_of_tuples)

#
# QUERY THE TABLE
#

print("-------------------")
query = f"SELECT * FROM {table_name};"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()
cursor.close()
connection.close()
