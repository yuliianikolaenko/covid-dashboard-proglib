import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


#functions
DATA = ('data.csv')
DATE_COLUMN = 'date'
@st.cache
def load_data():
    df = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])
    return df

def draw_map_cases():
    fig = px.choropleth(df, locations="iso_code",
                         color="total_cases",
                         hover_name="location",
                         title="Total COVID 19 cases in the world",
                         color_continuous_scale=px.colors.sequential.Redor)
    return fig

def draw_map_deaths():
    fig = px.choropleth(df, locations="iso_code",
                         color="total_deaths",
                         hover_name="location",
                         title="Total deaths from COVID 19 in the world",
                         color_continuous_scale=px.colors.sequential.Greys)
    return fig

def draw_map_vaccine():
    fig = px.choropleth(df, locations="iso_code",
                         color="total_vaccinations",
                         hover_name="location",
                         title="Total vaccinated from COVID 19 in the world",
                         color_continuous_scale=px.colors.sequential.Greens)
    return fig

st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")

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

show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")
    st.write(df)

# Calculate the timerange for the slider
min_ts = min(df[DATE_COLUMN]).to_pydatetime()
max_ts = max(df[DATE_COLUMN]).to_pydatetime()

##### SIDEBAR
#slider to chose date
show_timerange = st.sidebar.checkbox("Show date range")
if show_timerange:
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts])
    df = df[(df[DATE_COLUMN] >= min_selection) & (df[DATE_COLUMN] <= max_selection)]

#selectbox to chose between cases, deaths or total_vaccinations
select_event = st.sidebar.selectbox('Show map', ('total_cases', 'total_deaths', 'total_vaccinations'))
if select_event == 'total_cases':
    st.plotly_chart(draw_map_cases(), use_container_width=True)

if select_event == 'total_deaths':
    st.plotly_chart(draw_map_deaths(), use_container_width=True)

if select_event == 'total_vaccinations':
    st.plotly_chart(draw_map_vaccine(), use_container_width=True)



