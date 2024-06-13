import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create a SQLite database
conn = sqlite3.connect('nyanza_retail_sales.db')
cursor = conn.cursor()

# Drop the Sales table if it already exists
cursor.execute('DROP TABLE IF EXISTS Sales')

# Create the Sales table
cursor.execute('''
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    product_category TEXT,
    product_name TEXT,
    region TEXT,
    sales_amount REAL,
    quantity_sold INTEGER
)
''')

# Generate sample data
np.random.seed(0)

# Define parameters for the dataset
date_range = pd.date_range(start='2023-01-01', end='2023-12-31')
regions = ['Kisumu', 'Homa Bay', 'Migori', 'Kisii', 'Nyamira', 'Siaya', 'Bondo', 'Rongo']
categories = {
    'Electronics': ['HP Laptop', 'Dell Laptop', 'Lenovo Laptop', 'Asus Laptop', 'Acer Laptop', 'Samsung Laptop', 'Apple Laptop', 'Sony Laptop', 'Microsoft Laptop', 'Toshiba Laptop'],
    'Clothing': ['Shirt', 'Jeans', 'Jacket', 'Dress', 'Skirt', 'T-Shirt', 'Shorts', 'Sweater', 'Blouse', 'Coat'],
    'Home & Kitchen': ['Cookware', 'Furniture', 'Decor', 'Bedding', 'Utensils', 'Appliances', 'Tableware', 'Storage', 'Cleaning Supplies', 'Lighting'],
    'Books': ['Fiction Book', 'Non-Fiction Book', 'Children Book', 'Comics', 'Magazine', 'Textbook', 'Notebook', 'Biography', 'Poetry', 'Science Book'],
    'Toys': ['Action Figure', 'Doll', 'Puzzle', 'Board Game', 'Toy Car', 'Building Blocks', 'Plush Toy', 'Educational Toy', 'Outdoor Toy', 'Electronic Toy'],
    'Sports': ['Football', 'Basketball', 'Tennis Racket', 'Running Shoes', 'Gym Equipment', 'Yoga Mat', 'Cricket Bat', 'Baseball Glove', 'Swimming Gear', 'Cycling Gear'],
    'Beauty': ['Skincare Product', 'Makeup Product', 'Perfume', 'Haircare Product', 'Nail Polish', 'Body Lotion', 'Face Mask', 'Lipstick', 'Sunscreen', 'Eyeliner'],
    'Health': ['Vitamins', 'Supplements', 'First Aid Kit', 'Medical Equipment', 'Health Monitor', 'Personal Care', 'OTC Medicine', 'Herbal Remedies', 'Fitness Tracker', 'Pain Relief']
}

# Generate sample data
data = []
for date in date_range:
    for region in regions:
        for category, products in categories.items():
            for product in products:
                sales_amount = round(np.random.uniform(10, 500), 2)
                quantity_sold = np.random.randint(1, 20)
                data.append((date.strftime('%Y-%m-%d'), category, product, region, sales_amount, quantity_sold))

# Insert data into the Sales table
cursor.executemany('''
INSERT INTO Sales (date, product_category, product_name, region, sales_amount, quantity_sold)
VALUES (?, ?, ?, ?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()
