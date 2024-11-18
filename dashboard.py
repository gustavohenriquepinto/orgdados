import pandas as pd
import streamlit as st
import datetime

class Dashboard:
  results_df = pd.DataFrame
  goalscorers_df = pd.DataFrame
  shootouts_df = pd.DataFrame
  
  COUNTRIES : list[str]
  
  country : str
  initial_date : datetime.date
  final_date : datetime.date
  
  def read_datasets(self) -> None:
    self.results_df = pd.read_csv('results.csv')
    self.goalscorers_df = pd.read_csv('goalscorers.csv')
    self.shootouts_df = pd.read_csv('shootouts.csv')
    
    self.COUNTRIES = self.get_countries()

  def get_countries(self) -> pd.Series[str]:
    return ['Todos'] + sorted(pd.concat([
      self.results_df['home_team'],
      self.results_df['away_team'],
      self.goalscorers_df['home_team'],
      self.goalscorers_df['away_team'],
      self.shootouts_df['home_team'],
      self.shootouts_df['away_team'],
    ]).unique().tolist())
  
  def show_filters(self) -> None:
    self.country = st.sidebar.selectbox('País', self.COUNTRIES)
    self.initial_date = st.sidebar.date_input('Início', value=datetime.date(1872,1,1), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
    self.final_date = st.sidebar.date_input('Fim', value=datetime.date(2024,12,31), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
  
  def apply_filters(self) -> None:   
    self.results_df = self.results_df[(self.results_df['date'] >= self.initial_date.strftime('%Y-%m-%d')) & (self.results_df['date'] <= self.final_date.strftime('%Y-%m-%d'))]
    self.goalscorers_df = self.goalscorers_df[(self.goalscorers_df['date'] >= self.initial_date.strftime('%Y-%m-%d')) & (self.goalscorers_df['date'] <= self.final_date.strftime('%Y-%m-%d'))]
    self.shootouts_df = self.shootouts_df[(self.shootouts_df['date'] >= self.initial_date.strftime('%Y-%m-%d')) & (self.shootouts_df['date'] <= self.final_date.strftime('%Y-%m-%d'))]

  def show_dashboard(self) -> None:
    self.chart_main_host()
  
    top_scorer = self.goalscorers_df['scorer'].value_counts()
    own_goals = self.goalscorers_df['own_goal'].value_counts()

    st.bar_chart(top_scorer) # Maiores artilheiros
    st.bar_chart(own_goals) # Artilheiros de gol-contra
  

  
  def chart_main_host(self) -> None:
    data = self.results_df[self.results_df['country'] == self.country] if self.country != 'Todos' else self.results_df
    data = data['country'].value_counts()
    
    if data.empty:
      st.write('Esse país nunca sediou uma partida!')
      return
    
    st.bar_chart(data)
  
  
  
  