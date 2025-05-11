import streamlit as st
import pandas as pd
import plotly.express as px

st.title("E-commerce Sales Sheet Analysis Deshboard")

def load_data(file_path):
    data = pd.read_csv(file_path)
    data["Date"] = pd.to_datetime(data["Date"],errors="coerce")
    data=data.dropna(subset=["Date"])   #remove rows with invalid date
    return data
data_path = "./supermarket_sales.csv"

data = load_data(data_path)

st.dataframe(data.head(3))

#side bar for filters
st.sidebar.header("Filters")

select_branch = st.sidebar.multiselect("Select Branch",options=data["Branch"].unique(),default=data["Branch"].unique())
select_product = st.sidebar.multiselect("Select product",options=data["Product line"].unique())
select_customer = st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique())

# data["Date"].dtype
# st.write

min_date = data["Date"].min().date()
max_date = data["Date"].max().date()
select_date = st.sidebar.date_input("Select Date Range",value=(min_date,max_date),min_value=min_date,max_value=max_date)

filtered_data = data[(data["Branch"].isin(select_branch)) & data["Product line"].isin(select_product) & data["Date"].isin(select_date)]

st.dataframe(filtered_data)

filtered_data["Total"] = filtered_data["Total"].round(2)
filtered_data["gross income"] = filtered_data["gross income"].round(2)
filtered_data["Rating"] = filtered_data["Rating"].round(2)
filtered_data["Quantity"] = filtered_data["Quantity"].round(2)


#streamlit key_matrics
total_sale = filtered_data["Total"].sum()
gross_income = filtered_data["gross income"].sum()
total_quantity = filtered_data["Quantity"].sum()
avg_rating = filtered_data["Rating"].mean()

st.subheader("KPI/Key Matrics")
col1,col2,col3,col4 = st.columns(4)


with col1:
    st.metric(label="Total Sales",value=f"{total_sale}")

with col2:
    st.metric(label="gross_income",value=f"{gross_income}")

with col3:
    st.metric(label="total_quantity",value=f"{total_quantity}")

with col4:
    st.metric(label="avg_rating",value=f"{avg_rating}")



sales_by_branch = filtered_data.groupby("Branch")["Total"].sum().reset_index()

st.subheader("Total sales by Branch")
fig_branch = px.bar(
    sales_by_branch,x="Branch",y="Total",
    title="Total sales by Branch",
    text="Total",
    color="Branch"
)
st.subheader("Total sale by Branch")
fig_branch = px.bar(
    sales_by_branch, x="Branch",y="Total",
    title="Total Sales By Branch",
    text="Total",
    color="Branch"
)
st.plotly_chart(fig_branch)