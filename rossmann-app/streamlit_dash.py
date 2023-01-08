import pandas as pd
import numpy as np
import streamlit as st
import requests
import json

from datetime import datetime

def make_prediction(data):
    # convert Dataframe to json
    json_data = json.dumps( data.to_dict( orient='records' ) )

    # API Call
    url = 'https://rossmann-sales-forecast.onrender.com/rossmann/predict'
    header = {'Content-type': 'application/json' }
    data = json_data

    r = requests.post( url, data=data, headers=header )

    if r.status_code == 200:
        d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )

        return f"Store Number {d1.loc[0, 'store']} will most likely sell ${d1.loc[0, 'prediction']:,.2f} in {d1.loc[0, 'date'].split('T')[0].replace('-', '/')}"
    else:
        st.write(r.status_code)

        return 'Erro'

def main():
    st.set_page_config(layout='wide', page_title='Real Time Sales Prediction', page_icon='🏪')

    st.title('Rossman Store Sales Forecast')
    st.markdown('Este aplicativo prevê o valor de vendas de uma Loja em um determinado dia. Apenas preencha as informações da Loja e clique no botão "Predict".')
    
    # Store ID input
    st.markdown("## New Store ID")
    input_store_id = st.number_input("ID (optional)", value=0)

    # Date input
    min_date = datetime(year=2015, month=8, day=1)
    max_date = datetime(year=2015, month=9, day=17)
    st.markdown("## Date")
    input_date = st.date_input('Day of the Sale', value=min_date, min_value=min_date, max_value=max_date)

    # Promo input
    st.markdown("## Promo")
    input_promo = st.radio("Store is holding a Tradicional Promotion?", [1, 0], format_func=lambda x: 'Yes' if x == 1 else 'No', index=0)

    # State Holiday input
    state_holiday_dict = {'regular_day': 'Regular Day', 'public_holiday': 'Public Holiday', 'easter_holiday': "Easter's Holiday", "christmas": "Christma's Holiday"}

    st.markdown("## State Holiday")
    input_state_holiday = st.selectbox("The select date is a state holiday?", ['regular_day', 'public_holiday', "easter_holiday", "christmas"], format_func=lambda x: state_holiday_dict.get(x), index=0)

    # School Holiday input
    st.markdown("## School Holiday")
    input_school_holiday = st.radio("The select date is a school holiday?", [1, 0], format_func=lambda x: 'Yes' if x == 1 else 'No', index=0)

    # Store Type input

    st.markdown("## Store Type")
    input_store_type = st.selectbox("Select the type of the Store", ['a', 'b', "c", "d"], index=0)

    # Assortment input
    assortment_dict = {'basic': 'Basic', 'extended': 'Extended', 'extra': 'Extra'}

    st.markdown("## Assortment Level")
    input_assortment = st.selectbox("Level of assortment", ['basic', 'extended', 'extra'], format_func=lambda x: assortment_dict.get(x), index=0)

    # Competition Distance input
    st.markdown("## Competition Distance")
    input_competition_distance = st.slider('Distance between closest competitor Store', 0, 20000, 0, key='competition_distance')

    # Competition Open Since (Year and Month) input
    st.markdown("## Competition Open Since Year")
    input_competition_open_year = st.slider('Year that the first competitor store was open', 1900, 2015, 1900, key='competition_open_since_year')

    st.markdown("## Competition Open Since Month")
    input_competition_open_month = st.slider('Month that the first competitor store was open', 1, 12, 1, key='competition_open_since_month')

    # Promo 2 input
    st.markdown("## Promo2")
    input_promo2 = st.radio("Store is holding any Extended Promotions?", [1, 0], format_func=lambda x: 'Yes' if x == 1 else 'No', index=0)

    # Promo 2 Since (Year and Week) input
    st.markdown("## Promo2 Since Year")
    input_promo2_since_year = st.slider('Year that the extended promotion started', 2009, 2015, 2009, key='promo2_since_year')

    st.markdown("## Promo2 Since Week of Year")
    input_promo2_since_week = st.slider('Week of year that the extended promotion started', 1, 52, 1, key='promo2_since_week')

    # Promo Interval input
    st.markdown("## Promo Interval")
    input_promo_interval = st.multiselect("Months of renovation for Extended Promotions", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], default=["Jan", "Apr", "Jul", "Oct"], max_selections=4)

    # Data
    data = pd.DataFrame({
        'store': input_store_id,
        'day_of_week': pd.to_datetime(input_date).day_of_week,
        'date': datetime.strftime(input_date, format='%Y-%m-%d'), 
        'open': 1, 
        'promo': input_promo, 
        'state_holiday': input_state_holiday,
        'school_holiday': input_school_holiday,
        'store_type': input_store_type, 
        'assortment': input_assortment, 
        'competition_distance': input_competition_distance,
        'competition_open_since_year': input_competition_open_year, 
        'competition_open_since_month': input_competition_open_month, 
        'promo2': input_promo2, 
        'promo2_since_year': input_promo2_since_year,
        'promo2_since_week': input_promo2_since_week, 
        'promo_interval': ','.join(input_promo_interval)}, index=[0])

    st.write("Data Preview:")
    st.dataframe(data)

    st.write("")
    st.write("")

    # Prediction Button
    pred_message = ""

    c1, c2, c3 = st.columns((1, 1, 1))

    with c2:
        st.markdown("<h5 style='text-align:center;font-size:15px'>Let the Magic Happen 🎩🪄</h5>", unsafe_allow_html=True)

        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            width: 100%;
            font-weight: bolder;
            position: relative;
            bottom: 20px;
            border-color: #e84440;
            color: #e84440;
            border-width: 2px;
        }
        div.stButton > button:hover {
            background-color: #e84440;
            color: white;
        }
        </style>""", unsafe_allow_html=True)

        if st.button("Make Prediction"):
            pred_message = make_prediction(data)

    st.markdown(f"# {pred_message}")


if __name__ == '__main__':
    main()