import streamlit as st
from utils import load_data

########################## LOAD DATA ##########################

ev_sales_df, ev_charging_points_df = load_data()

########################## HEADER ##########################    

st.header("Charging Points")

st.divider()

########################## CHARGING POINTS HISTOGRAM ##########################