from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import create_db
from database import execute_query, fetch_query

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder= 'nandhini')
app.secret_key = 'secretkey'
create_db()

# 1. User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        try:
            execute_query('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password))
            return redirect(url_for('login'))
        except:
            return "Username already exists!"
    return render_template('register.html')

# 2. User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = fetch_query('SELECT * FROM Users WHERE username = ?', (username,))
        if user and check_password_hash(user[0][2], password):
            session['user_id'] = user[0][0]
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials!"
    return render_template('login.html')

# 3. Home Page with Product Search and Filter
@app.route('/')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query', '')
    seasonal = request.args.get('seasonal', None)

    sql_query = '''
        SELECT p.product_id, p.name AS product_name, p.price, a.name AS allergen_name
        FROM Products p
        LEFT JOIN Product_Allergen pa ON p.product_id = pa.product_id
        LEFT JOIN Allergens a ON pa.allergen_id = a.allergen_id
        WHERE p.name LIKE ?
    '''
    params = [f"%{query}%"]
    
    if seasonal:
        sql_query += ' AND p.seasonal = ?'
        params.append(seasonal)

    products = fetch_query(sql_query, params)

    # Organize products by their allergens
    product_data = {}
    for product in products:
        product_id = product[0]
        if product_id not in product_data:
            product_data[product_id] = {
                'product_name': product[1],
                'price': product[2],
                'allergens': []
            }
        if product[3]:
            product_data[product_id]['allergens'].append(product[3])

    return render_template('home.html', products=product_data, username=session['username'])

# 4. Add Product to Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    quantity = int(request.form.get('quantity', 1))
    user_id = session['user_id']
    
    execute_query('INSERT INTO Cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
    return redirect(url_for('view_cart'))

# 5. View Cart
# @app.route('/cart')
# def view_cart():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     user_id = session['user_id']
#     cart_items = fetch_query('''
#         SELECT c.cart_id, p.name, c.quantity, p.price, (c.quantity * p.price) AS total_price
#         FROM Cart c
#         JOIN Products p ON c.product_id = p.product_id
#         WHERE c.user_id = ?
#     ''', (user_id,))
#     total_price = sum(item[2] * item[3] for item in cart_items)
#     return render_template('cart.html', cart_items=cart_items)
@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    # Handle removing item from the cart
    if request.method == 'POST':
        cart_id_to_remove = request.form.get('cart_id')
        execute_query('DELETE FROM Cart WHERE cart_id = ?', (cart_id_to_remove,))

    # Fetch the cart items
    cart_items = fetch_query('''
        SELECT c.cart_id, p.name, c.quantity, p.price
        FROM Cart c
        JOIN Products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
    ''', (user_id,))
    
    # Calculate total price
    total_price = sum(item[2] * item[3] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)
@app.route('/add_allergen', methods=['GET', 'POST'])
def add_allergen():
    if request.method == 'POST':
        product_id = request.form['product_id']
        allergen_name = request.form['allergen_name']

        # Check if the allergen already exists in the database
        allergen = fetch_query('SELECT allergen_id FROM Allergens WHERE name = ?', (allergen_name,))
        if not allergen:
            # If it doesn't exist, insert it
            execute_query('INSERT INTO Allergens (name) VALUES (?)', (allergen_name,))
            allergen = fetch_query('SELECT allergen_id FROM Allergens WHERE name = ?', (allergen_name,))

        # Get allergen ID and link it to the product
        allergen_id = allergen[0][0]
        execute_query('INSERT INTO Product_Allergen (product_id, allergen_id) VALUES (?, ?)', (product_id, allergen_id))
        return f"Allergen '{allergen_name}' added to product {product_id}!"

    return render_template('add_allergen.html')

@app.route('/product/<int:product_id>')
def product_details(product_id):
    # Fetch allergens linked to the product
    allergens = fetch_query('''
        SELECT a.name
        FROM Product_Allergen pa
        JOIN Allergens a ON pa.allergen_id = a.allergen_id
        WHERE pa.product_id = ?
    ''', (product_id,))
    return render_template('product_details.html', allergens=allergens)
# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    from database import create_db  # Import create_db
    create_db() 
    app.run(debug=True)
