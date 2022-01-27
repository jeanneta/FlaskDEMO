from distutils.log import debug
from flask import Flask, app, render_template, request, redirect, url_for, jsonify
import psycopg2 #pip install psycopg2 
import psycopg2.extras

app=Flask(__name__)

#connect to the DB 
con=psycopg2.connect(
    host      = "localhost",
    database  = "postgres",
    user      = "postgres",
    password  = "1234"
)

@app.route('/')
def Index():
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "select * from data_clustering"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)


  
@app.route("/searchdata",methods=["POST","GET"])
def searchdata():
    if request.method == 'POST':
        search_word = request.form['search_word']
        print(search_word)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM data_clustering WHERE name LIKE %(name)s', { 'name': '%{}%'.format(search_word)})
        data_clustering = cur.fetchall()
    return jsonify({'data': render_template('layout.html', data_clustering=data_clustering)})

if __name__ == "__main__":
    app.run(debug=True)
