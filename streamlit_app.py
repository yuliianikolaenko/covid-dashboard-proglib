import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json

#functions
DATA = ('data.csv')
DATE_COLUMN = 'date'
@st.cache
def load_data():
    df = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])
    return df

with urlopen('https://storage.googleapis.com/kagglesdsdata/datasets/4456/6834/world-countries.json?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20210609%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20210609T153957Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=13594c9ddedccd436258d48a33dcd74195dcd598a8330ffc5f86b669ca8c744260e0db0ef9e00771989fadab546b45fe5bcf8ab0f882ec554d50488544eafcae313c57548815b3af7fcaaeafab309a95ac263680e6b5ad50a77422414cabf2b14a7e3a37486db7ec29f77428ee48a3d568d3375ec7f3a5f460001d41bde1c62514bfa195e3853fd6a5f9b046ae47f14ddd5bc35f9a33607d4eb080a1554522ba3a443f72c06a1896b8f617da4cc4b5762bff0c3c64ed739fe89669eae0011220895406f43ba81fd6ad8000eb5b53b328c2f170caee41dfeb8448c9982ea6ab3e2878200d195c2cf15e4d9e40574a8fe411f075e47b44f923524ea86e022f850f') as response:
    counties = json.load(response)

def draw_map_cases():
    fig = px.choropleth_mapbox(df, geojson=counties, locations='iso_code', color='total_cases',
                               color_continuous_scale="Redor",
                               mapbox_style="carto-positron",
                               title = "Total COVID 19 cases in the world",
                               zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def draw_map_deaths():
    fig = px.choropleth_mapbox(df, geojson=counties, locations='iso_code', color='total_deaths',
                               color_continuous_scale="Greys",
                               mapbox_style="carto-positron",
                               title = "Total deaths from COVID 19  in the world",
                               zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

def draw_map_vaccine():
    fig = px.choropleth_mapbox(df, geojson=counties, locations='iso_code', color='total_vaccinations',
                               color_continuous_scale="Greens",
                               mapbox_style="carto-positron",
                               title = "Total vaccinations from COVID 19 in the world",
                               zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
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



##### SIDEBAR
#slider to chose date
show_timerange = st.sidebar.checkbox("Show date range")
if show_timerange == True:
    # Calculate the timerange for the slider
    min_ts = min(df[DATE_COLUMN]).to_pydatetime()
    max_ts = max(df[DATE_COLUMN]).to_pydatetime()
    day_date = pd.to_datetime(st.sidebar.slider("Date to chose", min_value=min_ts, max_value=max_ts, value=max_ts))
    st.write(f"Data for {day_date.date()}")
    df = df[(df['date'] == day_date)]
    st.write(f"Data Points:{len(df)}")

    #df = df[(df[DATE_COLUMN] >= min_selection) & (df[DATE_COLUMN] <= max_selection)]#.groupby('iso_code').mean()[['total_cases','total_deaths','total_vaccinations']]

#selectbox to chose between cases, deaths or total_vaccinations
select_event = st.sidebar.selectbox('Show map', ('total_cases', 'total_deaths', 'total_vaccinations'))
if select_event == 'total_cases':
    st.plotly_chart(draw_map_cases(), use_container_width=True)

if select_event == 'total_deaths':
    st.plotly_chart(draw_map_deaths(), use_container_width=True)

if select_event == 'total_vaccinations':
    st.plotly_chart(draw_map_vaccine(), use_container_width=True)



