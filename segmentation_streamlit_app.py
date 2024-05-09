import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\ismai\Desktop\PROJ3-E-Commerce Data\data.csv', encoding="ISO-8859-1")
    return df

data = load_data()



# Convert 'InvoiceDate' column to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Extract year, month, and day and add them as separate columns
data['Year'] = data['InvoiceDate'].dt.year
data['Month'] = data['InvoiceDate'].dt.month
data['Day'] = data['InvoiceDate'].dt.day

year_10 = data.query('Year ==2010')['Quantity'].sum()
year_11 = data.query('Year ==2011')['Quantity'].sum()

data['SalesRevenue'] = data['Quantity'] * data['UnitPrice']


# Define functions for analysis
def quantity_and_revenue():
    datas = {
        'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'Quantity': [308966, 277989, 351872, 289098, 380391, 341623, 391116, 406199, 549817, 570532, 740286, 568561],
        'SalesRevenue': [560000.26, 498062.65, 683267.08, 493207.12, 723333.51, 691123.12, 681300.11, 682680.51, 1019687.622, 1070704.67, 1461756.25, 1182625.03]
    }

    # Create DataFrame
    dfs = pd.DataFrame(datas)

    # Plotting the bar chart
    st.bar_chart(dfs.set_index('Month'))




def stockcode_most_sold(data):
    stockcode_counts = data['StockCode'].value_counts().head(20)
    st.bar_chart(stockcode_counts)

def most_description(data):
    description_counts = data['Description'].value_counts().head(20)
    st.bar_chart(description_counts, color='#CA8787')
    st.table(description_counts)

def most_customer(data):
    customer_counts = data['CustomerID'].value_counts().head(20)
    st.bar_chart(customer_counts)
    

def cancelled_transaction(data):
    cancelled_transactions = data['InvoiceNo'].str.startswith('C').sum()
    total_transactions = len(data['InvoiceNo'])
    cancelled_percentage = (cancelled_transactions / total_transactions) * 100
    
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie([cancelled_percentage, 100 - cancelled_percentage], labels=['Cancelled Transactions', 'Non-cancelled Transactions'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(fig)

# Define function for quantity sold by year analysis
def quantity_sold_by_year(data):
    # Convert 'InvoiceDate' column to datetime format
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    # Extract year, month, and day and add them as separate columns
    data['Year'] = data['InvoiceDate'].dt.year

    year_10 = data.query('Year == 2010')['Quantity'].sum()
    year_11 = data.query('Year == 2011')['Quantity'].sum()

    # Prepare data for bar chart
    chart_data = pd.DataFrame({
        'Year': ['2010', '2011'],
        'Quantity Sold': [year_10, year_11]
    })

    # Display bar chart using st.bar_chart
    st.info(f"Quantity sold in 2010: {year_10:,.2f}$")
    st.info(f"Quantity sold in 2011: {year_11:,.2f}$")
    st.bar_chart(chart_data.set_index('Year') , color=['#ff66b3'])

def revenue_copar_Qsolde(data):
    data['SalesRevenue'] = data['Quantity'] * data['UnitPrice']
    # Convert 'InvoiceDate' column to datetime format
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['Month'] = data['InvoiceDate'].dt.month

    monthly_data = data.groupby('Month').agg({'Quantity': 'sum', 'SalesRevenue': 'sum'})
    st.line_chart(monthly_data)
    quantity_and_revenue()

def revenue_by_month(data):

    # Convert 'InvoiceDate' column to datetime format
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['Month'] = data['InvoiceDate'].dt.month
    data['SalesRevenue'] = data['Quantity'] * data['UnitPrice']
    monthly_revenue = data.groupby('Month')['SalesRevenue'].sum()
    st.bar_chart(monthly_revenue)
    st.write(monthly_revenue)

def top_copany_by_revenue(data):
    data['SalesRevenue'] = data['Quantity'] * data['UnitPrice']
    top_countries = data.groupby('Country')['SalesRevenue'].sum().nlargest(10)
    st.bar_chart(top_countries)
    st.write(top_countries)


# Create DataFrame for features description
columns_dict = {
       'InvoiceNo': 'Code representing each unique transaction. If this code starts with letter "c", it indicates a cancellation.',
       'StockCode': 'Code uniquely assigned to each distinct product.',
       'Description': 'Description of each product.',
       'Quantity': 'The number of units of a product in a transaction.',
       'InvoiceDate': 'The date and time of the transaction.',
       'UnitPrice': 'The unit price of the product in sterling.',
       'CustomerID': 'Identifier uniquely assigned to each customer.',
       'Country': 'The country of the customer.'
       }

df_description = pd.DataFrame(columns_dict.items(), columns=['Column Name', 'Description'])


# Create DataFrame for new segmentation data
columns_dict = {
    'CustomerID': 'Identifier uniquely assigned to each customer, used to distinguish individual customers.',
    'Days_Since_Last_Purchase': 'The number of days that have passed since the customer\'s last purchase.',
    'Total_Transactions': 'The total number of transactions made by the customer.',
    'Total_Products_Purchased': 'The total quantity of products purchased by the customer across all transactions.',
    'Total_Spend': 'The total amount of money the customer has spent across all transactions.',
    'Average_Transaction_Value': 'The average value of the customer\'s transactions, calculated as total spend divided by the number of transactions.',
    'Unique_Products_Purchased': 'The number of different products the customer has purchased.',
    'Average_Days_Between_Purchases': 'The average number of days between consecutive purchases made by the customer.',
    'Day_Of_Week': 'The day of the week when the customer prefers to shop, represented numerically (0 for Monday, 6 for Sunday).',
    'Hour': 'The hour of the day when the customer prefers to shop, represented in a 24-hour format.',
    'Is_UK': 'A binary variable indicating whether the customer is based in the UK (1) or not (0).',
    'Cancellation_Frequency': 'The total number of transactions that the customer has cancelled.',
    'Cancellation_Rate': 'The proportion of transactions that the customer has cancelled, calculated as cancellation frequency divided by total transactions.',
    'Monthly_Spending_Mean': 'The average monthly spending of the customer.',
    'Monthly_Spending_Std': 'The standard deviation of the customer\'s monthly spending, indicating the variability in their spending pattern.',
    'Spending_Trend': 'A numerical representation of the trend in the customer\'s spending over time. A positive value indicates an increasing trend, a negative value indicates a decreasing trend, and a value close to zero indicates a stable trend.'
}

# Create DataFrame from dictionary
new_df_description = pd.DataFrame(columns_dict.items(), columns=['Column Name', 'Description'])



# Streamlit app

#  Navigation bar
selected_page = st.sidebar.selectbox(
    "Explore E-Commerce Data",
    options=["Data Analysis", "Customer Recommendations (Coming Soon)"]
)

# Based on selected page, perform the appropriate analysis
if selected_page == "Data Analysis":
    st.title('E-Commerce Data Analysis')
    
    # Sidebar navigation
    nav_selection = st.sidebar.radio("Navigation", ("Overview", "Stockcode Most Sold", "Most Common Product",
                                                    "Most Common Customers", "Cancelled Transactions",
                                                    "Quantity Sold by Year", "Revenue Compared to Quantity Sold",
                                                    "Revenue by Month", "Top 10 Countries by Revenue"
                                                    ))
    
    # Load data
    if nav_selection != "Overview":
        data = load_data()
    
    # Overview
    if nav_selection == "Overview":
        st.subheader("Data Overview")
        st.write("Total Rows:", len(data))
        st.write('Total Columns:',len(data.columns))
        st.write(data.head())
        st.table(df_description)
    # Analysis based on user selection
    elif nav_selection == "Stockcode Most Sold":
        st.subheader("Stockcode Most Sold")
        stockcode_most_sold(data)
    
    elif nav_selection == "Most Common Product":
        st.subheader("Most 20 Common Product")
        most_description(data)
    
    elif nav_selection == "Most Common Customers":
        st.subheader("Most Common Customers")
        most_customer(data)
    
    elif nav_selection == "Cancelled Transactions":
        st.subheader("Cancelled Transactions")
        cancelled_transaction(data)
    
    elif nav_selection == "Quantity Sold by Year":
        st.subheader("Quantity Sold by Year")
        quantity_sold_by_year(data)
    
    elif nav_selection == "Revenue Compared to Quantity Sold":
        st.subheader("Revenue Compared to Quantity Sold by Month")
        revenue_copar_Qsolde(data)
    
    elif nav_selection == "Revenue by Month":
        st.subheader("Revenue by Month")
        revenue_by_month(data)
    
    elif nav_selection == "Top 10 Countries by Revenue":
        st.subheader("Top 10 Countries by Revenue")
        top_copany_by_revenue(data)
    
elif selected_page == "Customer Recommendations (Coming Soon)":
    st.subheader("Data Overview")
    st.write("Total Rows:", len(new_df_description))
    st.subheader('Columns Descriptions')
    st.table(new_df_description)