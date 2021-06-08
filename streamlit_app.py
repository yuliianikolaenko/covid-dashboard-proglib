import streamlit as st
import pandas as pd
import plotly.express as px


#Titles and Mode selections
st.sidebar.title("Menu")
st.sidebar.radio("Navigate", ["Home", "Data", "Dashboard", "About"])
selectbox = st.sidebar.selectbox('Type',('death','case'))
st.sidebar.title("About")
st.sidebar.info(
    """
    This app in Open Source
    """
)
st.sidebar.title("Comment")
st.sidebar.info("Feel free to comment on work. The github link can be found "
                "[here]()")


st.title("COVID DASHBOARD")
st.write("""
This web application will serve to analyze and visualize the spread of COVID-19""")
st.markdown("## Symptoms")
st.markdown(("* Fever or chills\n* Cough\n"
             "* Shortness of breath or difficulty breathing\n"
             "* Fatigue\n"
             "* Muscle or body aches\n"
             "* Headache\n"
             "* Loss of taste or smell\n"
             "* Sore throat\n"
             "* Congestion or runny nose\n"
             "* Nausea or vomiting\n"
             "* Diarrhea"))


st.image('covid.jpeg')

#Load Data
df_case = pd.read_csv('Clean_Confirmed_Case.csv')
df_case = df_case.set_index(['Date'])
df_Death = pd.read_csv('Clean_Death.csv')
df_Death = df_Death.set_index(['Date'])
df_Recovered = pd.read_csv('Clean_Recovered.csv')
df_Recovered = df_Recovered.set_index(['Date'])


#Chart the Datas
selectbox = st.sidebar.selectbox('Type',('death','case'))


if selectbox == 'death':
    st.title("Cumulative number of deaths")
    case = st.multiselect('choose country',df_case.columns)

    print(case)

    fig = px.line(df_case, x=df_case.index, y=case)
    st.write(fig)
else:
    st.title("Cumulative number of cases")
    death = st.multiselect('choose country', df_Death.columns)

    print(death)

    fig = px.line(df_Death, x=df_Death.index, y=death)
    st.write(fig)
