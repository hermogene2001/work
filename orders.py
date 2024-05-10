from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'infocus'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/order', methods=['POST'])
def place_order():
    if request.method == 'POST':
        service = request.form['service']
        date = request.form['date']

        # Insert order into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (service, date) VALUES (%s, %s)", (service, date))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
