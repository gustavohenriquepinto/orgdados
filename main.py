import pandas as pd
import streamlit as st
import datetime

results_df : pd.DataFrame
goalscorers_df : pd.DataFrame
shootouts_df : pd.DataFrame

COUNTRIES : list[str]

country : str
initial_date : datetime.date
final_date : datetime.date

def read_datasets() -> None:
  results_df = pd.read_csv('results.csv')
  goalscorers_df = pd.read_csv('goalscorers.csv')
  shootouts_df = pd.read_csv('shootouts.csv')
  
def get_countries() -> list[str]:
  return ['Todos'] + sorted(pd.concat([
    results_df['home_team'],
    results_df['away_team'],
    goalscorers_df['home_team'],
    goalscorers_df['away_team'],
    shootouts_df['home_team'],
    shootouts_df['away_team'],
 ]).unique().tolist())

read_datasets()

def show_filters() -> None:
  country = st.sidebar.selectbox('País', COUNTRIES)
  initial_date = st.sidebar.date_input('Início', value=datetime.date(1872,1,1), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
  final_date = st.sidebar.date_input('Fim', value=datetime.date(2024,12,31), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
  
  def apply_date_filters() -> None:   
    results_df = results_df[(results_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (results_df['date'] <= final_date.strftime('%Y-%m-%d'))]
    goalscorers_df = goalscorers_df[(goalscorers_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (goalscorers_df['date'] <= final_date.strftime('%Y-%m-%d'))]
    shootouts_df = shootouts_df[(shootouts_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (shootouts_df['date'] <= final_date.strftime('%Y-%m-%d'))]
  
  apply_date_filters()

def show_dashboard() -> None:
  def chart_main_host() -> None:
    data = results_df[results_df['country'] == country] if country != 'Todos' else results_df
    data = data['country'].value_counts()
  
    if data.empty:
      st.write('Esse país nunca sediou uma partida!')
      return
  
    st.bar_chart(data)
  def chart_top_scorers() -> None:
    pass

  def chart_own_goals() -> None:
      pass
  

read_datasets()
COUNTRIES = get_countries()
show_dashboard()
  
  