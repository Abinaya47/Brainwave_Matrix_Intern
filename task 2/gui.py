import tkinter as tk
from tkinter import messagebox, simpledialog
import auth
import inventory

BACKGROUND_COLOR = '#e6f2ff'  # light blue-ish
BUTTON_COLOR = '#ffffff'      # white
BUTTON_FONT = ('Arial', 12)
ENTRY_FONT = ('Arial', 12)
LABEL_FONT = ('Arial', 12)
TITLE_FONT = ('Arial', 16, 'bold')

def show_login(root):
    """Display the login window."""
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x180")
    login_win.configure(bg=BACKGROUND_COLOR)
    login_win.resizable(False, False)

    # Username
    tk.Label(login_win, text="Username:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    username_entry = tk.Entry(login_win, font=ENTRY_FONT)
    username_entry.pack(pady=5)

    # Password
    tk.Label(login_win, text="Password:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    password_entry = tk.Entry(login_win, show="*", font=ENTRY_FONT)
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if auth.authenticate(username, password):
            messagebox.showinfo("Login", "Login successful!")
            login_win.destroy()
            root.deiconify()
            build_main_ui(root)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    login_button = tk.Button(login_win, text="Login", command=attempt_login,
                             font=BUTTON_FONT, bg=BUTTON_COLOR)
    login_button.pack(pady=10)

    # Make the login window modal
    login_win.grab_set()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    login_win.protocol("WM_DELETE_WINDOW", root.destroy)

def on_add():
    """Handle adding a new product."""
    add_win = tk.Toplevel()
    add_win.title("Add Product")
    add_win.geometry("300x250")
    add_win.configure(bg=BACKGROUND_COLOR)
    add_win.resizable(False, False)

    tk.Label(add_win, text="Product Name:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    name_entry = tk.Entry(add_win, font=ENTRY_FONT)
    name_entry.pack(pady=5)

    tk.Label(add_win, text="Quantity:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    qty_entry = tk.Entry(add_win, font=ENTRY_FONT)
    qty_entry.pack(pady=5)

    tk.Label(add_win, text="Price:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    price_entry = tk.Entry(add_win, font=ENTRY_FONT)
    price_entry.pack(pady=5)

    def save_product():
        name = name_entry.get().strip()
        qty = qty_entry.get().strip()
        price = price_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Product name is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return
        inventory.add_product(name, qty, price)
        messagebox.showinfo("Success", "Product added successfully.")
        add_win.destroy()

    tk.Button(add_win, text="Add", command=save_product,
              font=BUTTON_FONT, bg=BUTTON_COLOR, width=10).pack(pady=15)

def on_edit():
    """Handle editing an existing product."""
    product_id = simpledialog.askinteger("Edit Product", "Enter Product ID:")
    if product_id is None:
        return
    product = inventory.get_product(product_id)
    if not product:
        messagebox.showerror("Error", f"No product found with ID {product_id}.")
        return

    edit_win = tk.Toplevel()
    edit_win.title("Edit Product")
    edit_win.geometry("300x250")
    edit_win.configure(bg=BACKGROUND_COLOR)
    edit_win.resizable(False, False)

    tk.Label(edit_win, text="Product Name:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    name_entry = tk.Entry(edit_win, font=ENTRY_FONT)
    name_entry.pack(pady=5)
    name_entry.insert(0, product[1])

    tk.Label(edit_win, text="Quantity:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    qty_entry = tk.Entry(edit_win, font=ENTRY_FONT)
    qty_entry.pack(pady=5)
    qty_entry.insert(0, product[2])

    tk.Label(edit_win, text="Price:", font=LABEL_FONT, bg=BACKGROUND_COLOR).pack(pady=(10,0))
    price_entry = tk.Entry(edit_win, font=ENTRY_FONT)
    price_entry.pack(pady=5)
    price_entry.insert(0, product[3])

    def update_product():
        name = name_entry.get().strip()
        qty = qty_entry.get().strip()
        price = price_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Product name is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return
        inventory.edit_product(product_id, name, qty, price)
        messagebox.showinfo("Success", "Product updated successfully.")
        edit_win.destroy()

    tk.Button(edit_win, text="Update", command=update_product,
              font=BUTTON_FONT, bg=BUTTON_COLOR, width=10).pack(pady=15)

def on_delete():
    """Handle deleting a product."""
    product_id = simpledialog.askinteger("Delete Product", "Enter Product ID:")
    if product_id is None:
        return
    product = inventory.get_product(product_id)
    if not product:
        messagebox.showerror("Error", f"No product found with ID {product_id}.")
        return
    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{product[1]}'?")
    if confirm:
        inventory.delete_product(product_id)
        messagebox.showinfo("Deleted", "Product deleted successfully.")

def on_view():
    """Display all products."""
    products = inventory.get_all_products()
    if not products:
        messagebox.showinfo("Products", "No products found.")
        return
    info = ""
    for prod in products:
        info += f"ID: {prod[0]}, Name: {prod[1]}, Quantity: {prod[2]}, Price: ${prod[3]:.2f}\n"
    messagebox.showinfo("Products", info)

def on_low_stock():
    """Display products with low stock."""
    threshold = simpledialog.askinteger("Low Stock Alert", "Enter stock threshold:", minvalue=1)
    if threshold is None:
        return
    low_products = inventory.get_low_stock(threshold)
    if not low_products:
        messagebox.showinfo("Low Stock", "No products below the threshold.")
        return
    info = ""
    for prod in low_products:
        info += f"ID: {prod[0]}, Name: {prod[1]}, Quantity: {prod[2]}\n"
    messagebox.showinfo("Low Stock Products", info)

def on_sales_summary():
    """Display a basic sales summary (total inventory value)."""
    products = inventory.get_all_products()
    total_items = sum(prod[2] for prod in products)
    total_value = sum(prod[2] * prod[3] for prod in products)
    summary = f"Total Products: {len(products)}\nTotal Items in Stock: {total_items}\nTotal Inventory Value: ${total_value:.2f}"
    messagebox.showinfo("Sales Summary", summary)

def on_logout(root):
    """Handle user logout."""
    confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if confirm:
        # Clear main UI widgets
        for widget in root.winfo_children():
            widget.destroy()
        # Show login window again
        root.withdraw()
        show_login(root)

def build_main_ui(root):
    """Build the main UI after successful login."""
    root.title("Inventory Management System")
    root.geometry("600x400")
    root.configure(bg=BACKGROUND_COLOR)

    welcome_label = tk.Label(root, text="Welcome, brainwave!", font=TITLE_FONT, bg=BACKGROUND_COLOR)
    welcome_label.pack(pady=10)

    button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    button_frame.pack(pady=20)

    # Add Product
    add_btn = tk.Button(button_frame, text="Add Product", font=BUTTON_FONT,
                        bg=BUTTON_COLOR, width=15, command=on_add)
    add_btn.grid(row=0, column=0, padx=10, pady=10)

    # Edit Product
    edit_btn = tk.Button(button_frame, text="Edit Product", font=BUTTON_FONT,
                         bg=BUTTON_COLOR, width=15, command=on_edit)
    edit_btn.grid(row=0, column=1, padx=10, pady=10)

    # Delete Product
    delete_btn = tk.Button(button_frame, text="Delete Product", font=BUTTON_FONT,
                           bg=BUTTON_COLOR, width=15, command=on_delete)
    delete_btn.grid(row=0, column=2, padx=10, pady=10)

    # View Products
    view_btn = tk.Button(button_frame, text="View Products", font=BUTTON_FONT,
                         bg=BUTTON_COLOR, width=15, command=on_view)
    view_btn.grid(row=1, column=0, padx=10, pady=10)

    # Low Stock Alert
    lowstock_btn = tk.Button(button_frame, text="Low Stock Alert", font=BUTTON_FONT,
                             bg=BUTTON_COLOR, width=15, command=on_low_stock)
    lowstock_btn.grid(row=1, column=1, padx=10, pady=10)

    # Sales Summary
    sales_btn = tk.Button(button_frame, text="Sales Summary", font=BUTTON_FONT,
                          bg=BUTTON_COLOR, width=15, command=on_sales_summary)
    sales_btn.grid(row=1, column=2, padx=10, pady=10)

    # Logout
    logout_btn = tk.Button(root, text="Logout", font=BUTTON_FONT,
                           bg=BUTTON_COLOR, width=10, command=lambda: on_logout(root))
    logout_btn.pack(side=tk.BOTTOM, pady=15)

def start_app():
    """Start the inventory management application."""
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("600x400")
    root.withdraw()  # hide the main window initially

    show_login(root)

    root.mainloop()

if __name__ == '__main__':
    start_app()
