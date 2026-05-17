from flask import Flask,render_template
import pandas as pd
import sqlite3
import os

app=Flask(__name__)

df=pd.read_excel("full_aptitude_questions.xlsx")

values=[]

for _,row in df.iterrows():
    values.append((
        row["Question"],
        row["Option A"],
        row["Option B"],
        row["Option C"],
        row["Option D"],
        row["Answer"],
        row["Explanation"]
    ))

def create_table():
    conn=sqlite3.connect("aptitude.db")
    cursor=conn.cursor()

    cursor.execute("create table if not exists software (id integer primary key autoincrement,question text not null,opt1 text not null, opt2 text not null, opt3 text not null, opt4 text not null,answer number not null,Explanation text not null)")

    conn.commit()
    conn.close()

create_table()

def insert_table():
    conn=sqlite3.connect("aptitude.db")
    cursor=conn.cursor()

    cursor.executemany("insert or ignore into software (question,opt1,opt2,opt3,opt4,answer,explanation) values(?,?,?,?,?,?,?)",(values))

    conn.commit()
    conn.close()

insert_table()

@app.route('/')
def home():
    
    return render_template("aptitude_home.html",values=values)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))