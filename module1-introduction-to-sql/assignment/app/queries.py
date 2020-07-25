# modeule1-introduction-to-sql/assignment/app/queries.py

import os
import sqlite3
import pandas as pd

conn = os.path.join(os.path.dirname(__file__), "..", "data", "rpg_db.sqlite3")
conn.row_factory = sqlite3.Row
print(type(conn))

curs = conn.cursor()
print(type(curs))

# Character counts
query_char = """Select count(distinct character_id) From
charactercreator_character as char_cre_char"""
num_char = curs.execute(query_char).fetchone()
print("Number of distinct Characters: ", num_char[0])
print("--------------")

# Subclass counts
query_cleric = """Select count(distinct(character_ptr_id)) from
charactercreator_cleric"""
num_cleric = curs.execute(query_cleric).fetchone()
print("Number of Clerics: ", num_cleric[0])

query_mage = """Select count(distinct(character_ptr_id)) from
charactercreator_mage"""
num_mage = curs.execute(query_mage).fetchone()
print("Number of Mages: ", num_mage[0])

query_theif = """Select count(distinct(character_ptr_id)) from
 charactercreator_thief"""
num_theif = curs.execute(query_theif).fetchone()
print("Number of Theives: ", num_theif[0])

query_fighter = """Select count(distinct(character_ptr_id)) from
charactercreator_fighter"""
num_fighter = curs.execute(query_fighter).fetchone()
print("Number of Fighters: ", num_fighter[0])

query_necro = """Select count(distinct(mage_ptr_id)) from
charactercreator_necromancer"""
num_necro = curs.execute(query_necro).fetchone()
print("Number of Necromancers: ", num_necro[0])
print("--------------")

# # Total items
query_items = "Select count(item_id) from armory_item"
total_item_results = curs.execute(query_items).fetchone()
print("Number of items: ", total_item_results[0])

# Number of Weapons
query_weapons = "Select count(item_ptr_id) from armory_weapon"
weapon_item_results = curs.execute(query_weapons).fetchone()
print("Items that are weapons: ", weapon_item_results[0])

# Number of not weapons
not_weapons = total_item_results[0] - weapon_item_results[0]
print("Items that are non-weapons: ", not_weapons)
print("--------------")

# Number of items and weapons per character
# first 20 lines
char_items = '''
Select
   ccc.name,
   count(distinct(cci.item_id)) as item_count,
   count(distinct(aw.item_ptr_id)) as weapon_count
from charactercreator_character_inventory cci
left join charactercreator_character ccc on cci.character_id = ccc.character_id
left join armory_item ai on cci.item_id = ai.item_id
left join armory_weapon aw on cci.item_id=aw.item_ptr_id
group by 1
limit 20;
'''
pack_results = curs.execute(char_items).fetchall()
for row in pack_results:
    name = row[0]
    print(f"{name} has {row[1]} items, {row[2]} of which are weapons")
print("--------------")

# Average number of items per Character
query_char_item_total = '''
Select
    COUNT(name)
From charactercreator_character;
'''
results_char_item_total = curs.execute(query_char_item_total).fetchall()
ave_num_items = results_char_item_total[0] / num_char[0]
print(f"Average number of items per Character: {ave_num_items}")

# Average number of weapons per Character
query_avg_weap_per_char = '''
SELECT AVG(Weapon_Count) as Average_weapons
From (
     SELECT
         cci.character_id,
         Count(aw.item_ptr_id) as Weapon_Count
     From charactercreator_character_inventory as cci
     LEFT Join armory_weapon AS aw ON cci.item_id == aw.item_ptr_id
     GROUP BY cci.character_id
    )
'''
results_avg_weap_per_char = curs.execute(query_avg_weap_per_char).fetchall()
print("Average number of weapons per character: ",
      results_avg_weap_per_char[0])
