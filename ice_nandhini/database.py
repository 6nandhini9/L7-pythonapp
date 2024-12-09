# database.py
import sqlite3
DB_NAME = "ice_cream_nandhini.db"

def create_connection():
    """Create a database connection."""
    return sqlite3.connect('ice_cream_nandhini.db')

def execute_query(query, params=None):
    """Execute a query that modifies data (INSERT, UPDATE, DELETE)."""
    conn = create_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

def fetch_query(query, params=None):
    """Execute a query that fetches data (SELECT)."""
    conn = create_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def create_db():
    """Create tables if they do not exist."""
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    '''

    create_products_table = '''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT NOT NULL,
        seasonal BOOLEAN NOT NULL
    );
    '''

    create_cart_table = '''
    CREATE TABLE IF NOT EXISTS Cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES Users(id),
        FOREIGN KEY(product_id) REFERENCES Products(product_id)
    );
    '''
    create_allergens_table = '''
    CREATE TABLE IF NOT EXISTS Allergens (
        allergen_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    '''

    create_product_allergen_table = '''
    CREATE TABLE IF NOT EXISTS Product_Allergen (
        product_id INTEGER NOT NULL,
        allergen_id INTEGER NOT NULL,
        FOREIGN KEY(product_id) REFERENCES Products(product_id),
        FOREIGN KEY(allergen_id) REFERENCES Allergens(allergen_id),
        PRIMARY KEY (product_id, allergen_id)
    );
    '''

    execute_query(create_users_table)
    execute_query(create_products_table)
    execute_query(create_cart_table)
    execute_query(create_allergens_table)
    execute_query(create_product_allergen_table)
    print("Database and tables created successfully!")
