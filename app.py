
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px 



st.title('Life Expectancy vs GNI per capita')

@st.cache 
def data_p():
    ley = pd.read_csv("Data/life_expectancy_years.csv")
    gni = pd.read_csv("Data/gnipercapita_ppp_current_international.csv")
    pop = pd.read_csv("Data/population_total.csv")
   
    ley.ffill(inplace=True)
    gni.ffill(inplace=True)
    gni.backfill(inplace=True)

    gni_ty = pd.melt(gni, ["country"], var_name=["year"], value_name="GNI per capita")
    pop_ty = pd.melt(pop, ["country"], var_name=["year"], value_name="population")
    ley_ty = pd.melt(ley, ["country"], var_name=["year"], value_name="life expectancy")

    ley_gni_ty = pd.merge(ley_ty, gni_ty, how= 'left', on=['country', 'year'])
    merged_ty = pd.merge(ley_gni_ty, pop_ty, how= 'left', on=['country', 'year'])

    return merged_ty

merged_ty = data_p()

max_year = int(merged_ty['year'].max())

year = st.sidebar.slider('Year', min_value = 1990, max_value= max_year)
year = str(year)

countries = st.multiselect('Select countries', merged_ty.country.unique())

mty = merged_ty.loc[lambda d: d['country'].isin(countries)]
mty = mty.loc[mty['year'] == year]

fig = px.scatter(mty, x='GNI per capita', y='life expectancy', size='population', color='population', hover_name='country', log_x=True, range_x=[1, 12000], range_y=[0, 90])
st.plotly_chart(fig)