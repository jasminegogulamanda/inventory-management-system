
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "inventory.db")


def connect_db():
    return sqlite3.connect(DATABASE)




def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    # Rename existing duplicate records safely.
    cursor.execute("""
        UPDATE products
        SET name = 'Basic Mouse'
        WHERE id = 2 AND LOWER(name) = 'mouse'
    """)

    cursor.execute("""
        UPDATE products
        SET name = 'Premium Mouse'
        WHERE id = 3 AND LOWER(name) = 'mouse'
    """)

    # Prevent duplicate names, ignoring letter case.
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        unique_product_name
        ON products(name COLLATE NOCASE)
    """)

    connection.commit()
    connection.close()



def add_product(name, price, quantity):
    name = name.strip()

    if not name:
        print("Product name cannot be empty.")
        return

    if price <= 0:
        print("Price must be greater than zero.")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        """, (name, price, quantity))

        connection.commit()
        print(name, "added successfully!")

    except sqlite3.IntegrityError:
        print("Product already exists!")

    finally:
        connection.close()


def display_products():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, price, quantity
        FROM products
        ORDER BY id
    """)

    products = cursor.fetchall()
    connection.close()

    print("\n--- INVENTORY LIST ---")

    if not products:
        print("No products available.")
        return

    for product in products:
        print(
            "ID:", product[0],
            "| Name:", product[1],
            "| Price:", product[2],
            "| Quantity:", product[3]
        )
def search_product(name):
    name = name.strip()

    if not name:
        print("Product name cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, name, price, quantity
            FROM products
            WHERE name COLLATE NOCASE = ?
        """, (name,))

        product = cursor.fetchone()

        if product is None:
            print("Product not found!")
        else:
            print("\n--- PRODUCT DETAILS ---")
            print("ID:", product[0])
            print("Name:", product[1])
            print("Price:", product[2])
            print("Quantity:", product[3])

    finally:
        connection.close()




def update_stock(name, sold_quantity):
    if sold_quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT quantity
            FROM products
            WHERE LOWER(name) = LOWER(?)
        """, (name.strip(),))

        product = cursor.fetchone()

        if product is None:
            print("Product not found!")
            return

        if sold_quantity > product[0]:
            print("Not enough stock available!")
            return

        cursor.execute("""
            UPDATE products
            SET quantity = quantity - ?
            WHERE LOWER(name) = LOWER(?)
        """, (sold_quantity, name.strip()))

        connection.commit()
        print("Stock updated successfully!")
        print("Remaining stock:", product[0] - sold_quantity)

    finally:
        connection.close()


def main():
    create_table()

    while True:
        print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
        print("1. Add Product")
        print("2. Display Products")
        print("3. Sell Product")
        print("4. Search Product")
        print("5. Exit")
        

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter product name: ").strip()

            try:
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                add_product(name, price, quantity)
            except ValueError:
                print("Enter a valid price and whole-number quantity.")

        elif choice == "2":
            display_products()

        elif choice == "3":
            name = input("Enter product name to sell: ").strip()

            try:
                sold_quantity = int(input("Enter quantity sold: "))
                update_stock(name, sold_quantity)
            except ValueError:
                print("Enter a valid whole number.")

        elif choice == "4":
            name = input("Enter product name to search: ")
            search_product(name)

        elif choice == "5":
            print("Thank you for using Inventory Management System!")
            break

        else:
            print("Invalid choice! Select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
