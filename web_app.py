
import os
import sqlite3
import streamlit as st

# Keep the database in the same folder as this Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventory.db")

st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide"
)

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_products():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name, price, quantity FROM products ORDER BY id"
        ).fetchall()

st.title("📦 Inventory Management System")
st.write("Manage products and monitor your stock.")

products = load_products()

# Dashboard metrics
total_products = len(products)
total_units = sum(product[3] for product in products)
inventory_value = sum(product[2] * product[3] for product in products)

col1, col2, col3 = st.columns(3)
col1.metric("Product Types", total_products)
col2.metric("Total Units in Stock", total_units)
col3.metric("Inventory Value", f"₹{inventory_value:,.2f}")

st.divider()

# Show inventory
st.subheader("Current Inventory")

if products:
    st.dataframe(
        [
            {
                "ID": product[0],
                "Product": product[1],
                "Price (₹)": product[2],
                "Quantity": product[3],
                "Stock Value (₹)": product[2] * product[3],
            }
            for product in products
        ],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No products found. Add your first product below.")

# Search
st.subheader("Search Products")
search_name = st.text_input("Enter a product name")

if search_name.strip():
    matches = [
        product for product in products
        if search_name.strip().casefold() in product[1].casefold()
    ]

    if matches:
        st.dataframe(
            [
                {
                    "ID": p[0],
                    "Product": p[1],
                    "Price (₹)": p[2],
                    "Quantity": p[3],
                }
                for p in matches
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No matching product found.")

st.divider()

# Add a product
st.subheader("Add New Product")

with st.form("add_product_form"):
    name = st.text_input("Product name")
    price = st.number_input("Price (₹)", min_value=0.01, step=1.0)
    quantity = st.number_input("Initial quantity", min_value=1, step=1)

    submitted = st.form_submit_button("Add Product")

    if submitted:
        if not name.strip():
            st.error("Product name cannot be empty.")
        else:
            try:
                with get_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO products (name, price, quantity)
                        VALUES (?, ?, ?)
                        """,
                        (name.strip(), price, quantity)
                    )
                st.success(f"Added {name.strip()} successfully.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("A product with that name already exists.")

# Sell stock
st.subheader("Record a Sale")

if products:
    product_options = {
        f"{p[1]} (Available: {p[3]})": p[0]
        for p in products
    }

    with st.form("sell_product_form"):
        selected_label = st.selectbox(
            "Select product", list(product_options.keys())
        )
        sold_quantity = st.number_input(
            "Quantity sold", min_value=1, step=1
        )

        sale_submitted = st.form_submit_button("Record Sale")

        if sale_submitted:
            product_id = product_options[selected_label]

            with get_connection() as conn:
                current = conn.execute(
                    "SELECT quantity FROM products WHERE id = ?",
                    (product_id,)
                ).fetchone()

                if current is None:
                    st.error("Product not found.")
                elif sold_quantity > current[0]:
                    st.error("Not enough stock available.")
                else:
                    conn.execute(
                        "UPDATE products SET quantity = quantity - ? "
                        "WHERE id = ?",
                        (sold_quantity, product_id)
                    )
                    st.success("Sale recorded and stock updated.")
                    st.rerun()
