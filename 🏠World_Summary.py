import streamlit as st
import plotly.express as px
from utils import load_data, world_ev_sales_metric_card, world_ev_sales_growth_metric_card, world_ev_charging_points_metric_card

########################## SETUP ##########################

st.set_page_config(
    page_title="EV Adoption Tracker",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="expanded"
)


########################## LOAD DATA ##########################

ev_sales_df, ev_charging_points_df = load_data()

########################## HEADER ##########################

st.title("🚗 EV Adoption Tracker 🔋")

st.subheader("Explore the global EV market")

with st.expander("About this dashboard"):
    st.markdown('''
        This dashboard provides a comprehensive view of the global EV market, including historical sales data, market share, and key metrics. Data is sourced in real time from the [International Energy Agency API](https://www.iea.org/data-and-statistics/data-tools/global-ev-data-explorer).
    ''')

st.write("")

########################## CARDS ##########################

# Create three columns
col1, col2, col3 = st.columns(3)

# Create cards
card1 = col1.container(border=True)
card2 = col2.container(border=True)
card3 = col3.container(border=True)

# Get current year
current_year = ev_sales_df["Year"].max()

# Metric Card 1: World EV Sales
total_sales_current_year, delta_previous_year = world_ev_sales_metric_card(ev_sales_df)

card1.metric(label=f"{current_year} Electric Car World Sales", value=f"{total_sales_current_year:.1f}M", delta=f"{delta_previous_year:.1f}M since {current_year - 1}")

# Metric Card 2: World EV Sales Growth
current_year_growth, previous_year_growth = world_ev_sales_growth_metric_card(ev_sales_df)
card2.metric(label=f"{current_year} World EV Sales Growth", value=f"{current_year_growth:.1%}", delta=f"{previous_year_growth:.1%} in {current_year - 1}")

# Metric Card 3: World EV Charging Points
total_charging_points_current_year, delta_previous_year = world_ev_charging_points_metric_card(ev_charging_points_df)

card3.metric(label=f"{current_year} World EV Charging Points", value=f"{total_charging_points_current_year:.1f}M", delta=f"{delta_previous_year:.1f}M since {current_year - 1}")

########################## SALES HISTOGRAM ##########################

st.write("")
st.subheader("World EV Sales")
st.divider()

# Filter the data for the "World" country
filtered_ev_sales_df = ev_sales_df[ev_sales_df["Region"] == 'World']
# Display the chart
st.bar_chart(
    filtered_ev_sales_df, 
    x="Year", 
    y="Cars Sold", 
    color="Powertrain", 
    x_label="Year", 
    y_label="Number of EVs sold (M)"
)

# Add a divider
st.divider()