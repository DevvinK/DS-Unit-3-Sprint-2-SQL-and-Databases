# module2-sql-for-analysis\app\elephant_queries.py

import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os

load_dotenv() #> loads contents of the .env file into the script's environment


DB_NAME= os.getenv("DB_NAME", default = "OOPS")
DB_USER= os.getenv("DB_USER", default = "OOPS")
DB_PASSWORD= os.getenv("DB_PASSWORD", default = "OOPS")
DB_HOST= os.getenv("DB_HOST", default = "OOPS")
 

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST)

cursor = connection.cursor(cursor_factory = DictCursor)
print("CURSOR", type(cursor))

cursor.execute("SELECT * FROM test_table;")

result = cursor.fetchall()
for row in result:
   print("----")
   print(type(row))
   print(row)