# module1-introduction-to-sql\assignment\app\make_pop.py
# python -m assignment.app.make_pop

import pandas as pd
import os
import sqlite3

csv = r"assignment\data\buddymove_holidayiq.csv"
df = pd.read_csv(csv)

conn = sqlite3.connect("buddymove_holidayiq.sqlite3")
conn.row_factory = sqlite3.Row
curs = conn.cursor()

# print(df.shape), prints (249,7)

if os.path.isfile("buddymove_holidayiq.sqlite3") is True:
    pass
else:
    df.to_sql('review', con=conn)

query_num_rows = '''
    Select
    COUNT(*)
From review
'''
result_num_rows = curs.execute(query_num_rows).fetchone()
print("Number of rows: ", result_num_rows[0])

query_nature_shop_over_100 = '''
Select
   Count(User_Id)
From review
WHERE Nature >= 100 AND Shopping >= 100
'''
result_nature_shop_over_100 = curs.execute(
   query_nature_shop_over_100).fetchone()
print("Number of users over 100 in nature and shopping: ",
      result_nature_shop_over_100[0])