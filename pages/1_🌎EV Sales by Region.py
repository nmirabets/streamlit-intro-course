import streamlit as st
import plotly.express as px
from utils import load_data, top_10_regions_by_ev_sales

########################## LOAD DATA ##########################

ev_sales_df, ev_charging_points_df = load_data()

########################## HEADER ##########################

st.header("EV Sales")

st.divider()

########################## SALES HISTOGRAM ##########################

st.subheader("EV Sales by Region")

# Get the index of the country "World", to set it as the default value in the dropdown
world_index = ev_sales_df["Region"].unique().tolist().index("World")

# Create a filter for the country
country_filter = st.selectbox("Select a country", ev_sales_df["Region"].unique(), index = world_index)
filtered_ev_sales_df = ev_sales_df[ev_sales_df["Region"] == country_filter]

# Add some space
st.write("")

# Display the chart
st.bar_chart(filtered_ev_sales_df, x="Year", y="Cars Sold", color="Powertrain", x_label="Year", y_label="Number of EVs sold (millions)")

# Add a divider
st.divider()

########################## TOP REGIONS BY SALES ##########################

current_year = ev_sales_df["Year"].max()

st.subheader(f"Top Sales by Country for {current_year}")

top_countries_ev_sales_df = top_10_regions_by_ev_sales(ev_sales_df)

# Create a layout with three columns, place the table in the middle one
col1, col2 = st.columns([2, 1])

# Create a Plotly pie chart
fig = px.pie(top_countries_ev_sales_df, 
             values='Cars Sold', 
             names='Region',
             title="EV Sales by Country")

col1.plotly_chart(fig, use_container_width=True)

# Display the table with the top 10 regions by EV sales
col2.dataframe(top_countries_ev_sales_df.head(10), hide_index=True)

# Add a divider
st.divider()

########################## SALES BY COUNTRY AND YEAR ##########################

st.subheader("EV Sales by Country and Year")

# Add a multiselect for the country
country_filter = st.multiselect("Select a country", ev_sales_df["Region"].unique(), default=["USA", "China", "Europe"])

# Create a filter for the year
powertrain_filter = st.selectbox("Select a powertrain", ev_sales_df["Powertrain"].unique())

# Filter the dataframe
filtered_ev_sales_df = ev_sales_df[(ev_sales_df["Region"].isin(country_filter)) & (ev_sales_df["Powertrain"] == powertrain_filter)]

st.line_chart(filtered_ev_sales_df, x="Year", y="Cars Sold", color="Region", x_label="Year", y_label="Number of EVs sold (millions)")
