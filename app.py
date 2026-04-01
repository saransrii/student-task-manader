from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)

# 🔥 GET DATABASE URL (from Railway or environment)
db_url = os.getenv("mysql://root:ZxkrFSSVVYvXBkjvwKwXnAcNZhlLPMUl@interchange.proxy.rlwy.net:12083/railway")

# 👉 fallback (your Railway MySQL URL)
if not db_url:
    db_url = "mmysql://root:ZxkrFSSVVYvXBkjvwKwXnAcNZhlLPMUl@interchange.proxy.rlwy.net:12083/railway"

url = urlparse(db_url)

# ✅ FUNCTION for DB connection (BEST PRACTICE)
def get_db_connection():
    return mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],   # remove '/'
        port=url.port
    )

# 🔹 HOME PAGE - READ
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', customers=data)

# 🔹 INSERT - CREATE
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customer (name, mobile, amount, location) VALUES (%s, %s, %s, %s)", 
            (name, mobile, amount, location)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

# 🔹 UPDATE
@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customer SET mobile=%s, amount=%s, location=%s WHERE name=%s", 
        (mobile, amount, location, name)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# 🔹 DELETE
@app.route('/delete/<string:name>')
def delete(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE name=%s", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# 🔥 RUN APP
if __name__ == "__main__":
    app.run(debug=True)