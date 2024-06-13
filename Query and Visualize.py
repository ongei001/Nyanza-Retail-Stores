import sqlite3
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Connect to the SQLite database
conn = sqlite3.connect('nyanza_retail_sales.db')

# Query data from the Sales table
df = pd.read_sql_query("SELECT * FROM Sales", conn)

# Close the database connection
conn.close()

# Total Sales Over Time
total_sales_over_time = df.groupby('date')['sales_amount'].sum().reset_index()
fig1 = px.line(total_sales_over_time, x='date', y='sales_amount', title='Total Sales Over Time')

# Sales by Category
sales_by_category = df.groupby('product_category')['sales_amount'].sum().reset_index()
fig2 = px.bar(sales_by_category, x='product_category', y='sales_amount', title='Sales by Category')

# Sales Distribution by Region
sales_by_region = df.groupby('region')['sales_amount'].sum().reset_index()
fig3 = px.pie(sales_by_region, values='sales_amount', names='region', title='Sales Distribution by Region')

# Sales by Product
sales_by_product = df.groupby('product_name')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False)
fig4 = px.bar(sales_by_product, x='product_name', y='sales_amount', title='Sales by Product')

# Monthly Sales Trend
df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
monthly_sales_trend = df.groupby('month')['sales_amount'].sum().reset_index()
fig5 = px.line(monthly_sales_trend, x='month', y='sales_amount', title='Monthly Sales Trend')

# Top 10 Selling Products
top_10_products = df.groupby('product_name')['quantity_sold'].sum().reset_index().sort_values(by='quantity_sold', ascending=False).head(10)
fig6 = px.bar(top_10_products, x='product_name', y='quantity_sold', title='Top 10 Selling Products')

# Category Sales Trends Over Time
category_sales_trend = df.groupby(['month', 'product_category'])['sales_amount'].sum().reset_index()
fig7 = px.line(category_sales_trend, x='month', y='sales_amount', color='product_category', title='Category Sales Trends Over Time')

# Monthly Sales by Region
monthly_sales_by_region = df.groupby(['month', 'region'])['sales_amount'].sum().reset_index()
fig8 = px.line(monthly_sales_by_region, x='month', y='sales_amount', color='region', title='Monthly Sales by Region')

# Combine all visualizations into a single dashboard
fig = make_subplots(
    rows=4, cols=2, 
    subplot_titles=('Total Sales Over Time', 'Sales by Category', 'Sales Distribution by Region', 'Sales by Product', 'Monthly Sales Trend', 'Top 10 Selling Products', 'Category Sales Trends Over Time', 'Monthly Sales by Region'),
    specs=[[{'type': 'xy'}, {'type': 'xy'}],
           [{'type': 'domain'}, {'type': 'xy'}],
           [{'type': 'xy'}, {'type': 'xy'}],
           [{'type': 'xy'}, {'type': 'xy'}]]
)

fig.add_trace(fig1['data'][0], row=1, col=1)
fig.add_trace(fig2['data'][0], row=1, col=2)
fig.add_trace(fig3['data'][0], row=2, col=1)
fig.add_trace(fig4['data'][0], row=2, col=2)
fig.add_trace(fig5['data'][0], row=3, col=1)
fig.add_trace(fig6['data'][0], row=3, col=2)
fig.add_trace(fig7['data'][0], row=4, col=1)
fig.add_trace(fig8['data'][0], row=4, col=2)

fig.update_layout(height=1200, width=1500, title_text="Nyanza Retail Sales Dashboard")

fig.show()
