import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#functions
def load_data():
    df = pd.read_csv('owid-covid-data.csv')
    df = df[df.location != 'World']
    df["date"] = pd.to_datetime(df["date"])
    return df

def draw_map(fig):
    fig = px.choropleth(df, locations="iso_code",
                         color="total_cases",
                         hover_name="location",
                         animation_frame="date",
                         title="Total COVID 19 cases in the world",
                         color_continuous_scale=px.colors.sequential.Redor)
    return fig

st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")
st.markdown("#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")

#Titles and Mode selections
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib).")


# Load data
df = load_data()

# Calculate the timerange for the slider
min_ts = min(df["date"]).to_pydatetime()
max_ts = max(df["date"]).to_pydatetime()

##### SIDEBAR
#selectbox to chose between cases, deaths or total_vaccinations
select_event = st.sidebar.selectbox('Show map', ('total_cases', 'total_deaths', 'total_vaccinations'))
if select_event == 'total_cases':
    st.plotly_chart(draw_map(df), use_container_width=True)

if select_event == 'total_deaths':
    st.plotly_chart(draw_map(df), use_container_width=True)

if select_event == 'vaccinations':
    st.plotly_chart(draw_map(df), use_container_width=True)

##### SIDEBAR
#slider to chose date
show_timerange = st.sidebar.checkbox("Show date range")
day_date = pd.to_datetime(st.sidebar.slider("Date to chose", min_value=min_ts, max_value=max_ts, value=max_ts))
select_country = st.sidebar.checkbox("Show countries")
select_country = st.sidebar.selectbox("Country", options=np.append([""], df['location'].sort_values().unique()), index=0)
if select_country != "":
    df_country = df[df['location'] == select_country]
    show_timerange = False

if show_timerange:
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts,
                                                     value=[min_ts, max_ts])

    # Filter data for timeframe
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
    df = df[(df["date"] >= min_selection) & (df["date"] <= max_selection)]

else:
    # Get last day data
    #     day_date = pd.to_datetime(year + month + day, format='%Y%m%d')
    df = df[(df["date"] == day_date)]

