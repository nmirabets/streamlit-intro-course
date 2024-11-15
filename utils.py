import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """
    Load the data from the IEA API
    """

    # IEA API URLs
    ev_sales_url = "https://api.iea.org/evs?parameters=EV%20sales&category=Historical&mode=Cars&csv=true"
    ev_charging_points_url = "https://api.iea.org/evs?parameters=EV%20charging%20points&category=Historical&mode=EV&csv=true"

    # Load the data from the IEA API
    ev_sales_df = pd.read_csv(ev_sales_url)
    ev_charging_points_df = pd.read_csv(ev_charging_points_url)

    # Split the df into ev_sales_df, ev_charging_points_df
    ev_sales_df = ev_sales_df[ev_sales_df['parameter'] == 'EV sales']
    ev_charging_points_df = ev_charging_points_df[ev_charging_points_df['parameter'] == 'EV charging points']

    # Drop the columns
    cols_to_drop = ['mode', 'category', 'parameter']
    ev_sales_df = ev_sales_df.drop(columns=cols_to_drop)
    ev_charging_points_df = ev_charging_points_df.drop(columns=cols_to_drop)

    # Rename the columns
    ev_sales_df = ev_sales_df.rename(columns={"value": "Cars Sold", "region": "Region", "year": "Year", "powertrain": "Powertrain"})
    ev_charging_points_df = ev_charging_points_df.rename(columns={"value": "Charging Points", "region": "Region", "year": "Year", "powertrain": "Powertrain"})

    print("Data loaded successfully")

    return ev_sales_df, ev_charging_points_df

# Metric card 1
def world_ev_sales_metric_card(ev_sales_df):
    """
    Get the last two years of data for the total EV sales metric card
    """
    world_ev_sales_df = ev_sales_df[ev_sales_df["Region"] == "World"]

    current_year = world_ev_sales_df["Year"].max()
    previous_year = current_year - 1

    world_ev_sales_previous_year = world_ev_sales_df.groupby("Year")["Cars Sold"].sum().loc[previous_year]
    world_ev_sales_current_year = world_ev_sales_df.groupby("Year")["Cars Sold"].sum().loc[current_year]

    delta_previous_year = world_ev_sales_current_year - world_ev_sales_previous_year

    # Convert to millions
    world_ev_sales_current_year = world_ev_sales_current_year / 1_000_000
    delta_previous_year = delta_previous_year / 1_000_000

    return world_ev_sales_current_year, delta_previous_year

# Metric card 2
def world_ev_sales_growth_metric_card(ev_sales_df):
    """
    Get the current and previous year of data for the World EV Sales Growth metric card
    """

    # Filter the data for the World region
    world_ev_sales_df = ev_sales_df[ev_sales_df["Region"] == "World"]

    # Get the current and previous year
    current_year = world_ev_sales_df["Year"].max()
    previous_year = current_year - 1
    previous_year_2 = previous_year - 1

    # Get the total sales for the current and previous year
    world_ev_sales_previous_year = world_ev_sales_df.groupby("Year")["Cars Sold"].sum().loc[previous_year]
    world_ev_sales_current_year = world_ev_sales_df.groupby("Year")["Cars Sold"].sum().loc[current_year]
    world_ev_sales_previous_year_2 = world_ev_sales_df.groupby("Year")["Cars Sold"].sum().loc[previous_year_2]

    # Current year growth
    current_year_growth = (world_ev_sales_current_year / world_ev_sales_previous_year) - 1
    # Previous year growth
    previous_year_growth = (world_ev_sales_previous_year / world_ev_sales_previous_year_2) - 1

    return current_year_growth, previous_year_growth

# Metric card 3
def world_ev_charging_points_metric_card(ev_charging_points_df):
    """
    Get the total EV charging points for the current and previous year
    """

    # Filter the data for the World region
    world_charging_points_df = ev_charging_points_df[ev_charging_points_df["Region"] == "World"]

    # Get the current and previous year
    current_year = world_charging_points_df["Year"].max()
    previous_year = current_year - 1    

    # Get the total charging points for the current and previous year
    world_charging_points_previous_year = world_charging_points_df.groupby("Year")["Charging Points"].sum().loc[previous_year]
    world_charging_points_current_year = world_charging_points_df.groupby("Year")["Charging Points"].sum().loc[current_year]

    # Calculate the delta between the current and previous year
    delta_previous_year = world_charging_points_current_year - world_charging_points_previous_year

    # Convert to millions
    world_charging_points_current_year = world_charging_points_current_year / 1_000_000
    delta_previous_year = delta_previous_year / 1_000_000

    return world_charging_points_current_year, delta_previous_year

# Top Regions by EV Sales
def top_10_regions_by_ev_sales(ev_sales_df):
    """
    Get the top n regions by EV sales
    """
    # Remove the regions that we don't want to include
    regions_to_remove = ['World', 'EU27', 'Europe', 'Rest of the world']
    ev_sales_df = ev_sales_df[~ev_sales_df["Region"].isin(regions_to_remove)]

    # Get the current year
    year = ev_sales_df["Year"].max()

    # Filter the data for the selected year
    ev_sales_df = ev_sales_df[ev_sales_df["Year"] == year]

    # Add up the values for each powertrain, reset index turns the Series into a DataFrame
    ev_sales_region_df = ev_sales_df.groupby(["Region"])["Cars Sold"].sum().reset_index()
    # Sort the values
    ev_sales_region_df = ev_sales_region_df.sort_values(by="Cars Sold", ascending=False)

    # Change data type to int
    ev_sales_region_df["Cars Sold"] = ev_sales_region_df["Cars Sold"].astype(int)

    # Reset index
    ev_sales_region_df = ev_sales_region_df.reset_index(drop=True)

    # Group together regions with less than 100,000 sales
    ev_sales_region_df.loc[ev_sales_region_df["Cars Sold"] < 100_000, "Region"] = "Rest of the world"

    return ev_sales_region_df