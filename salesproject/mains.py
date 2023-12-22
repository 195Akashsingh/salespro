import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm



st.set_page_config(page_title="Sales!!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Sample Super Store EDA")

#----------------------------------------------







df = pd.read_csv("train.csv")
print(df.head())
#st.write(df)
#----------------------------------------------

st.sidebar.header("Choose your filter:")
region = st.sidebar.multiselect("pick your Region", df["Region"].unique())

# Create for region
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create for state
state = st.sidebar.multiselect("pick your State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# Create for city
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

# Filter the data based on Region, State, and City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df3["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Display the filtered DataFrame
st.write(filtered_df)

#=====================================================================



fig=plt.figure(figsize=(10, 5))
hist_color = "#20B2AA" 
edge_color = "black"  
sns.histplot(df["Region"], color=hist_color, linewidth=2, edgecolor=edge_color)
sns.set_style("dark")
st.write(fig)

#==============================================================


fig_line = px.line(df, x='Order Date', y='Sales', title='Sales Over Time',
                   labels={'sales': 'Sales', 'order date': 'Order Date'})

st.subheader('Sales Over Time (Line Chart)')
st.plotly_chart(fig_line)


 #=========================================================1

fig = px.bar(df,x = 'Segment',y='Sales',title='Bar Chart showing Sales by Segment',labels={'sales':'sales','Segment':'Segment'})
st.write(fig)

#===============================10


fig_box = px.box(df, y='Sales', title='Box Plot of Sales',
                 labels={'Sales': 'Sales'})
st.write(fig_box)



# Trend line: Identifying trends or patterns in the data
fig_trend = px.scatter(df, x=df.index, y='Sales', trendline='ols', title='Trend Line of Sales',
                       labels={'Sales': 'Sales'})
st.write(fig_trend)




#====================2

# Geographical map: Sales by country
#fig_country = px.choropleth(df, locations='Country', locationmode='country names',
 #                           color='Sales', hover_name='Country',
#                            title='Sales by Country')
#
#st.write(fig_country)


#===============================================================3
category_sales = df.groupby('Category')['Sales'].sum().reset_index()

# Bar chart for Sales by Category
fig1=plt.figure(figsize=(10, 6))
plt.bar(category_sales['Category'], category_sales['Sales'])
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.title('Sales by Category')
st.write(fig1)


# Pie chart for Proportion of Sales by Category
fig2 = plt.figure(figsize=(8, 8))
plt.pie(category_sales['Sales'], labels=category_sales['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Sales by Category')
st.write(fig2)
#===================================================================4

# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Group by Customer Segment and calculate total sales
segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()

# Pie chart for Sales by Customer Segment
fig4=plt.figure(figsize=(8, 8))
plt.pie(segment_sales['Sales'], labels=segment_sales['Segment'], autopct='%1.1f%%', startangle=140)
plt.title('Sales by Customer Segment')
st.write(fig4)

#=========================================================5


# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Group by Shipping Mode and calculate total sales
shipping_sales = df.groupby('Ship Mode')['Sales'].sum().reset_index()

# Bar chart for Sales by Shipping Mode
fig5=plt.figure(figsize=(10, 6))
plt.bar(shipping_sales['Ship Mode'], shipping_sales['Sales'])
plt.xlabel('Shipping Mode')
plt.ylabel('Total Sales')
plt.title('Sales by Shipping Mode')
st.write(fig5)





# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Convert order date and ship date to datetime objects with the correct format
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

# Calculate shipping time (in days)
df['shipping_time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Create a histogram for Shipping Time
fig6 = plt.figure(figsize=(10, 6))
plt.hist(df['shipping_time'], bins=20, edgecolor='black')
plt.xlabel('Shipping Time (Days)')
plt.ylabel('Frequency')
plt.title('Distribution of Shipping Time')
st.write(fig6)


#=========================================================================6

# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Group by Product Name and calculate total sales
product_sales = df.groupby('Product Name')['Sales'].sum().reset_index()

# Sort by sales in descending order to get top-selling products
top_products = product_sales.sort_values(by='Sales', ascending=False).head(10)

# Bar chart for Top-Selling Products
fig7=plt.figure(figsize=(12, 6))
plt.bar(top_products['Product Name'], top_products['Sales'])
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.title('Top 10 Selling Products')
plt.xticks(rotation=45, ha='right')
st.write(fig7)


# Group by Product Category and calculate the count of unique products
category_distribution = df.groupby('Category')['Product ID'].nunique().reset_index()

# Pie chart for Product Category Distribution
fig8=plt.figure(figsize=(8, 8))
plt.pie(category_distribution['Product ID'], labels=category_distribution['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Product Category Distribution')
st.write(fig8)


#===================================================7


# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Create a histogram for Sales Distribution
fig99=plt.figure(figsize=(10, 6))
plt.hist(df['Sales'], bins=20, edgecolor='black')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.title('Distribution of Sales')
st.write(fig99)

#========================================8




# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Convert order date to datetime object
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Scatter plot for Sales and Order Date
fig55=plt.figure(figsize=(12, 6))
plt.scatter(df['Order Date'], df['Sales'], alpha=0.5)
plt.xlabel('Order Date')
plt.ylabel('Sales')
plt.title('Scatter Plot: Sales vs. Order Date')
st.write(fig55)


#===================================9


# Assuming df is your DataFrame with the given columns
# For simplicity, let's consider a small sample dataset

# Group by Customer Segment and calculate total sales
segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()

# Bar chart for Sales by Customer Segment
fig66=plt.figure(figsize=(10, 6))
plt.bar(segment_sales['Segment'], segment_sales['Sales'])
plt.xlabel('Customer Segment')
plt.ylabel('Total Sales')
plt.title('Sales by Customer Segment')
st.write(fig66)

#=============================================================================









# Assuming df is your DataFrame with the given columns

fig_country = px.choropleth(df, locations='Country', locationmode='country names',
                            color='Sales', hover_name='Country',
                            title='Sales by Country',
                            projection='natural earth')  # You can adjust the projection as needed

st.plotly_chart(fig_country)

