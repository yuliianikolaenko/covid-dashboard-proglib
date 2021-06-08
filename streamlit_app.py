import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime

#Titles and Mode selections
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib)")

st.sidebar.title("Menu")
st.sidebar.radio("Navigate", ["Intro", "Data", "Map"])
selectbox = st.sidebar.selectbox('Type',('Total Cases','Total Deaths', 'Total Vaccinations'))
select_type = st.sidebar.selectbox("Type", options=np.append([""], df['total_cases', 'total_deaths', 'total_vaccinations'])

if select_type != "":
    df_type = df[df['total_cases', 'total_deaths', 'total_vaccinations']]
    show_timerange = True
#st.image('covid.jpeg')

st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world""")
st.markdown("### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data)")

#Load Data
df = pd.read_csv('owid-covid-data.csv')
df = df[df.location != 'World']
df["date"] = pd.to_datetime(df["date"])
# Calculate the timerange for the slider
min_ts = min(df["date"]).to_pydatetime()
max_ts = max(df["date"]).to_pydatetime()

##### SIDEBAR
#slider to chose date
show_timerange = st.sidebar.checkbox("Show date range")
day_date = pd.to_datetime(st.sidebar.slider("Date to chose", min_value=min_ts, max_value=max_ts, value=max_ts))
select_country = st.sidebar.selectbox("Countries", options=np.append([""], df['location'].sort_values().unique()), index=0)

if select_country != "":
    df_country = df[df['location'] == select_country]
    show_timerange = True

if show_timerange:
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts,
                                                     value=[min_ts, max_ts])

    # Filter data for timeframe
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")

    df = df[(df["date"] >= min_selection) & (df["date"] <= max_selection)]
    st.write(f"Country: {len(df)}")

else:
    # Get last day data
    #     day_date = pd.to_datetime(year + month + day, format='%Y%m%d')
    st.write(f"Data for {day_date.date()}")
    df = df[(df["date"] == day_date)]
    st.write(f"Data Points: {len(df)}")


fig1 = px.choropleth(df, locations="iso_code",
                    color="total_cases",
                    hover_name="location",
                    animation_frame="date",
                    title = "Total COVID 19 cases in the world",
                    color_continuous_scale=px.colors.sequential.Redor)

fig1["layout"].pop("updatemenus")
st.plotly_chart(fig1)


fig2 = px.choropleth(df, locations="iso_code",
                    color="total_deaths",
                    hover_name="location",
                    animation_frame="date",
                    title = "Total deaths from COVID 19 in the world",
                    color_continuous_scale=px.colors.sequential.Greys)

fig2["layout"].pop("updatemenus")
st.plotly_chart(fig2)


fig3 = px.choropleth(df, locations="iso_code",
                    color="total_vaccinations",
                    hover_name="location",
                    animation_frame="date",
                    title = "Total vaccinated people in the world",
                    color_continuous_scale=px.colors.sequential.Greens)

fig3["layout"].pop("updatemenus")
st.plotly_chart(fig3)

