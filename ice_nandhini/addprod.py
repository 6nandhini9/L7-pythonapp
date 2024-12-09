import sqlite3

def insert_ice_cream_data():
    conn = sqlite3.connect('ice_cream_nandhini.db')
    cursor = conn.cursor()

    # Sample ice cream data
    products = [
        ('Vanilla Ice Cream', 5.99, 'Classic vanilla ice cream made with real vanilla beans', 0),
        ('Chocolate Ice Cream', 6.49, 'Rich chocolate ice cream with a creamy texture', 0),
        ('Strawberry Ice Cream', 5.99, 'Fresh strawberry ice cream made with real strawberries', 0),
        ('Mint Chocolate Chip', 6.99, 'Refreshing mint ice cream with chocolate chips', 0),
        ('Salted Caramel Ice Cream', 7.49, 'Delicious salted caramel ice cream with a hint of sea salt', 0),
        ('Peach Sorbet', 4.99, 'Fruity and refreshing peach sorbet, perfect for a summer day', 1)
    ]

    # Insert data into Products table
    cursor.executemany('''INSERT INTO Products (name, price, description, seasonal) VALUES (?, ?, ?, ?)''', products)

    conn.commit()
    conn.close()

# Run the function to insert data
insert_ice_cream_data()
