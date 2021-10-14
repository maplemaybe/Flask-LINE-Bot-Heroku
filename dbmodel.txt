import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a fishlinebot').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT * FROM alpaca_training;")#選擇資料表userdata
rows = cursor.fetchall() #讀出所有資料

for row in rows:   #將讀到的資料全部print出來
    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))
    
conn.commit()