import streamlit as st
import pandas as pd

st.title("Thales Smart Factory Dashboard")

df = pd.read_csv("../data/Thales_Group_Manufacturing.csv")

st.dataframe(df.head())
