from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Karthi@1234'
app.config['MYSQL_DB'] = 'real_estate'

mysql = MySQL(app)



@app.route('/')
def index():
    return render_template("index.html")


# GETTING VALUES

@app.route('/properties')
def get_properties():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Properties")
    properties = cur.fetchall()
    cur.close()
    return render_template('properties.html', properties=properties)


@app.route('/users')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)


@app.route('/transactions')
def get_transactions():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Transactions")
    transactions = cur.fetchall()
    cur.close()
    return render_template('transactions.html', transactions=transactions)


# ADDING VALUES

@app.route('/add/user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        user_type = request.form['user_type']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Users (user_id, username, email, password, phone, user_type) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, username, email, password, phone, user_type))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_users'))


@app.route('/add/property', methods=['POST'])
def add_property():
    if request.method == 'POST':
        property_id = request.form['property_id']
        address = request.form['address']
        price = request.form['price']
        property_type = request.form['property_type']
        owner_id = request.form['owner_id']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Properties (property_id, address, price, property_type, owner_id, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (property_id, address, price, property_type, owner_id, status))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_properties'))


@app.route('/add/transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        buyer_id = request.form['buyer_id']
        property_id = request.form['property_id']
        transaction_date = request.form['transaction_date']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Transactions (transaction_id, buyer_id, property_id, transaction_date, price) VALUES (%s, %s, %s, %s, %s)",
            (transaction_id, buyer_id, property_id, transaction_date, price))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_transactions'))


# UPDATING VALUES

@app.route('/update/user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        email = request.form.get('email')
        phone = request.form.get('phone')

        cur = mysql.connection.cursor()
        if email:
            cur.execute("UPDATE Users SET email = %s WHERE user_id = %s", (email, user_id))
        if phone:
            cur.execute("UPDATE Users SET phone = %s WHERE user_id = %s", (phone, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_users'))


@app.route('/update/property/status', methods=['POST'])
def update_property_status():
    if request.method == 'POST':
        property_id = request.form['property_id']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Properties SET status = %s WHERE property_id = %s", (status, property_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_properties'))


@app.route('/update/transaction/price', methods=['POST'])
def update_transaction_price():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Transactions SET price = %s WHERE transaction_id = %s", (price, transaction_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('get_transactions'))


# DELETING VALUES

@app.route('/delete/user/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_users'))


@app.route('/delete/property/<string:property_id>', methods=['POST'])
def delete_property(property_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Properties WHERE property_id = %s", (property_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_properties'))


@app.route('/delete/transaction/<string:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Transactions WHERE transaction_id = %s", (transaction_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_transactions'))


# Function to search properties based on criteria

@app.route('/search/properties', methods=['POST'])
def search_properties():
    min_price = request.form.get('min_price')
    max_price = request.form.get('max_price')
    property_type = request.form.get('property_type')
    location = request.form.get('location')

    query = "SELECT * FROM Properties WHERE 1=1"
    params = []

    if min_price:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)
    if property_type:
        query += " AND property_type = %s"
        params.append(property_type)
    if location:
        query += " AND address LIKE %s"
        params.append(f"%{location}%")

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()

    if results:
        return render_template('properties.html', properties=results)
    else:
        return render_template('properties.html', message="No properties found matching the criteria.")


if __name__ == '__main__':
    app.run(debug=True)
