# Inventory Management System

A Python-based Inventory Management System that stores product details and manages stock using an SQLite database.

## Features

- Add new products
- Display all products
- Search for a product by name
- Sell products and update stock
- Validate product prices and quantities
- Prevent duplicate product names, ignoring letter case
- Prevent sales when available stock is insufficient
- Store inventory data persistently using SQLite

## Technologies Used

- Python
- SQLite
- SQL
- Visual Studio Code
- Git and GitHub (for version control)

## Requirements

- Python 3 installed
- No external Python packages required for the current application

## How to Run

1. Clone or download the project.
2. Open the project folder in a terminal.
3. Run:

   ```bash
   python app.py
   ```

4. Select an option from the menu to manage inventory.

## Database

The application uses SQLite to store product IDs, names, prices, and quantities in `inventory.db`.

The database file is created in the project directory when the application runs.

## Project Status

Core inventory operations and product search have been implemented and tested locally. AWS deployment is planned as a future enhancement.