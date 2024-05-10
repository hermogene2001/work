from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'infocus'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        names = request.form['names']
        phone = request.form['phone']
        acc = request.form['acc']
        bank = request.form['bank']
        pin = request.form['pin'].encode('utf-8')

        cur = mysql.connection.cursor()

        cur.execute("INSERT into users(name,phoneNbr,AccNbr,bankname,pin) values (%s,%s,%s,%s,%s)",(names,phone,acc,bank,pin))
        mysql.connection.commit()
        cur.close()

        # Redirect to login page
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pin']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name = %s and pin = %s", (email,password))
        user_id = session.get('user_id')
        user = cur.fetchone()
        cur.close()

        if user:
            session['logged_in'] = True
            session['user_id'] = user_id
            session['user_name'] = user['name']
            session['user_pin'] = user['pin']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Name or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        # Fetch user's orders from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM orders")
        data =cur.fetchall()

        cur.close()

        return render_template('dashboard.html', orders=data)
    else:
        return redirect(url_for('login'))
@app.route('/order', methods=['POST'])
def order():
    
    if request.method == 'POST':
        service = request.form['service']
        date = request.form['date']
        session['service'] = service  # Store service in session
        
        # Insert order into the database
        user_id = session.get('user_id')
        if user_id:
            # Insert order into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `orders` (`user_id`, `date`, `service`) VALUES (%s, %s, %s)", (user_id, date,service ))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('payment'))
        else:
            # Handle case where user is not logged in
            return redirect(url_for('dashboard'))

@app.route('/payment')
def payment():
    
    if 'logged_in' in session:
        # Fetch service from session
        service = session.get('service', None)
        
        if service:
            # Fetch user's orders from database
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM payment where name like %s", (f'%{service}%',))
            data = cur.fetchall()
            cur.close()

        return render_template('payment.html', orders=data)
    else:
        return redirect(url_for('login'))
    return render_template('payment.html')
@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')
@app.route('/orders')
def orders():
    try:
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM orders")

        # Fetch all rows
        orders = cur.fetchall()

        # Close cursor
        cur.close()

        return render_template('orders.html', orders=orders)
    except Exception as e:
        return str(e)
@app.route('/process_payment', methods=['POST'])
def process_payment():
    if request.method == 'POST':
        # Retrieve payment information from the form
        card_number = request.form['card_number']
        expiry_date = request.form['expiry_date']
        cvv = request.form['cvv']
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM `payment` WHERE name ='%s'")

        # Fetch all rows
        orders = cur.fetchall()

        # Close cursor
        cur.close()
        
        print("Card Number:", card_number)
        print("Expiry Date:", expiry_date)
        print("CVV:", cvv)

        # You can redirect to a confirmation page or return a success message
        return "Payment processed successfully!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)
