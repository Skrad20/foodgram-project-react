#! /bin/bash
sqlite3 backend/db.sqlite3
.mode csv
.separator ';'
.import data/ingredients_1.csv ingredients
exit