import pandas as pd
import streamlit as st
import datetime

# results_base = pd.read_csv('results.csv')
# goalscorers_base = pd.read_csv('goalscorers.csv')
# shootouts_base = pd.read_csv('shootouts.csv')

# results_conditions = None
# goalscorers_conditions = None
# shootouts_conditions = None

results_df = pd.read_csv('results.csv')
goalscorers_df = pd.read_csv('goalscorers.csv')
shootouts_df = pd.read_csv('shootouts.csv')

initial_date = st.sidebar.date_input('Início', min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
final_date = st.sidebar.date_input('Fim', min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))

# best_shootout_winner = 

