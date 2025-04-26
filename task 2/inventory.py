import sqlite3

# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create products table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()

def add_product(name, quantity, price):
    """Add a new product to the inventory."""
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
              (name, quantity, price))
    conn.commit()

def edit_product(product_id, name, quantity, price):
    """Edit an existing product's details."""
    c.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?",
              (name, quantity, price, product_id))
    conn.commit()

def delete_product(product_id):
    """Delete a product from the inventory by its ID."""
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

def get_all_products():
    """Return a list of all products as (id, name, quantity, price)."""
    c.execute("SELECT id, name, quantity, price FROM products")
    return c.fetchall()

def get_low_stock(threshold):
    """Return products with quantity below the given threshold."""
    c.execute("SELECT id, name, quantity FROM products WHERE quantity < ?", (threshold,))
    return c.fetchall()

def get_inventory_value():
    """Return the total inventory value (sum of quantity * price for all products)."""
    c.execute("SELECT SUM(quantity * price) FROM products")
    result = c.fetchone()[0]
    return result if result is not None else 0.0

def get_product(product_id):
    """Return product details by ID."""
    c.execute("SELECT id, name, quantity, price FROM products WHERE id = ?", (product_id,))
    return c.fetchone()
