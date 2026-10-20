# Cloud-Ready Inventory Management System

A Python-based inventory management application with a Streamlit web dashboard, SQLite database, and Docker containerization. The project is being prepared for cloud deployment.

## Features

- Add and manage products
- Search inventory by product name
- Record sales and update stock quantities
- Validate product details and stock availability
- Prevent duplicate product names
- Display total product types, stock units, and inventory value
- Store inventory data using SQLite
- Run the web application inside a Docker container

## Technologies Used

- Python
- SQLite and SQL
- Streamlit
- Docker
- Git and GitHub
- Visual Studio Code

## Run the Terminal Application

```bash
python app.py
```

## Run the Web Dashboard Locally

Install the required dependency:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run web_app.py
```

Open `http://localhost:8501` in your browser.

## Run with Docker

Build the image:

```bash
docker build -t inventory-management .
```

Run the container with the local database mounted:

```powershell
docker run --name inventory-dashboard -p 8501:8501 --mount "type=bind,source=$((Resolve-Path .\inventory.db).Path),target=/app/inventory.db" inventory-management
```

## Database

The application currently uses SQLite to store product IDs, names, prices, and quantities. The local database file is excluded from Git to protect inventory data.

## Project Status

The terminal application and Streamlit dashboard have been tested locally. The Docker image builds successfully, and database persistence has been tested with a container restart.

Cloud deployment and cloud-hosted persistent database integration are future enhancements.
