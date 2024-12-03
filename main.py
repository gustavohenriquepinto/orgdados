import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import datetime

plt.style.use('dark_background')

results_df : pd.DataFrame = pd.read_csv('results.csv')
goalscorers_df : pd.DataFrame = pd.read_csv('goalscorers.csv')
shootouts_df : pd.DataFrame = pd.read_csv('shootouts.csv')

TOURNAMENTS : list[str] = sorted(results_df['tournament'].unique().tolist())

PLAYERS : list[str] = sorted(goalscorers_df['scorer'].dropna().unique().tolist())

COUNTRIES : list[str] = sorted(pd.concat([
    results_df['home_team'],
    results_df['away_team'],
    results_df['country'],
    goalscorers_df['home_team'],
    goalscorers_df['away_team'],
    shootouts_df['home_team'],
    shootouts_df['away_team'],
]).unique().tolist())


initial_date : datetime.date = st.sidebar.date_input('Início', value=datetime.date(1872,1,1), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))
final_date : datetime.date = st.sidebar.date_input('Fim', value=datetime.date(2024,12,31), min_value=datetime.date(1872,1,1), max_value=datetime.date(2024,12,31))

# Impões os filtros de data sobre todos os dataframes
results_df = results_df[(results_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (results_df['date'] <= final_date.strftime('%Y-%m-%d'))]
goalscorers_df = goalscorers_df[(goalscorers_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (goalscorers_df['date'] <= final_date.strftime('%Y-%m-%d'))]
shootouts_df = shootouts_df[(shootouts_df['date'] >= initial_date.strftime('%Y-%m-%d')) & (shootouts_df['date'] <= final_date.strftime('%Y-%m-%d'))]
  
data : pd.DataFrame # Extração reduzida de dados a cada análise

################################

# 1. Times com mais vitórias
st.header('Grande Hall da Fama')
st.write('Descubra quais são os países com mais vitórias em cada torneio.')

tournament = st.selectbox('Torneio', ['Todos'] + TOURNAMENTS)
size_1 = st.number_input('Países', value = 0)

data = results_df[results_df['tournament'] == tournament] if tournament != 'Todos' else results_df

chart = pd.concat([
    data[data['home_score'] > data['away_score']]['home_team'],
    data[data['away_score'] > data['home_score']]['away_team'],
]).value_counts()

if size_1 > 0 and size_1 <  len(chart):
  chart = chart.head(size_1)

if chart.empty:
  st.write('Torneio sem partidas válidas!')
else:
  st.bar_chart(chart)

# 2. Relatório do país
st.header('Análise de País')
st.write('Utilize essa seção para obter um relatório sobre cada país.')

country_2 = st.selectbox('País', ['Nenhum'] + COUNTRIES)

skip_home_visitor_analysis = results_df[results_df['home_team'] == country_2].empty or results_df[results_df['away_team'] == country_2].empty

if country_2 == 'Nenhum':
  st.write('Selecione um país para analisar suas estatísticas.')

if not skip_home_visitor_analysis:
  data = results_df[(results_df['home_team'] == country_2) | (results_df['away_team'] == country_2)]

  home = data['home_team'] == country_2
  visitor = data['away_team'] == country_2
  draw = data['home_score'] == data['away_score']
  home_won = data['home_score'] > data['away_score']
  visitor_won = data['home_score'] < data['away_score']

  wins_home = len(data[(home) & (home_won)])
  draw_home = len(data[(home) & (draw)])
  lose_home = len(data[(home) & (visitor_won)])

  wins_visitor = len(data[(visitor) & (visitor_won)])
  draw_visitor = len(data[(visitor) & (draw)])
  lose_visitor = len(data[(visitor) & (home_won)])

  st.write(f'{country_2} tem um total de {len(home) + len(visitor)} partidas jogadas. Sendo {wins_home + wins_visitor} vitórias, {draw_home + draw_visitor} empates e {lose_home + lose_visitor} derrotas.')


  col1, col2 = st.columns(2)

  with col1:
    st.subheader(f'{country_2} em Casa')
    fig, ax = plt.subplots()
    ax.pie([wins_home, draw_home, lose_home], labels=['Vitórias', 'Empates', 'Derrotas'])
    ax.axis('equal')
    st.pyplot(fig)

    st.write(f'{country_2} tem {wins_home + draw_home + lose_home} partidas jogadas em casa.')
    st.write(f'Vitórias: {wins_home}')
    st.write(f'Empates: {draw_home}')
    st.write(f'Derrotas: {lose_home}')
  
  with col2:
    st.subheader(f'{country_2} como Visitante')
    fig, ax = plt.subplots()
    ax.pie([wins_visitor, draw_visitor, lose_visitor], labels=['Vitórias', 'Empates', 'Derrotas'])
    ax.axis('equal')
    st.pyplot(fig)

    st.write(f'{country_2} tem {wins_visitor + draw_visitor + lose_visitor} partidas jogadas como visitante.')
    st.write(f'Vitórias: {wins_visitor}')
    st.write(f'Empates: {draw_visitor}')
    st.write(f'Derrotas: {lose_visitor}')
elif country_2 != 'Nenhum':
  st.write(f'{country_2} não possui dados o suficiente para análise de partidas!')


# 3. Artilheiros
st.subheader('Artilheiros')
st.write('Os jogadores com mais gols em cada partida.')

country_3 = st.selectbox('País', ['Todos'] + COUNTRIES)
size_3 = st.number_input('Jogadores', value = 0)


data = goalscorers_df[goalscorers_df['team'] == country_3] if country_3 != 'Todos' else goalscorers_df
chart = data['scorer'].value_counts()

if size_3 > 0 and size_3 < len(chart):
  chart = chart.head(size_3)

if chart.empty:
  st.write(f'{country_3} não possui gols!')
else:
  st.bar_chart(chart)


# 4. Avaliação do Jogador

st.subheader('Avaliação do Jogador')

player = st.selectbox('Jogador', ['Nenhum'] + PLAYERS)

if player == 'Nenhum':
  st.write('Selecione um jogador!')
else:
  data = goalscorers_df[goalscorers_df['scorer'] == player]
  chart = data['date'].value_counts()


  if len(chart) < 2:
    st.write(f'{player} não tem dados suficientes para análise.')
  else:
    st.write(f'{player} tem um total de {len(data)} gols em sua carreira')
    st.area_chart(chart)


# 5. Decisões por pênalti

st.subheader('Decisões por Pênalti')

size_5 = st.number_input('Quantidade', 1, 5, 2)
_countries = st.multiselect('Países', COUNTRIES)

if len(_countries) != size_5:
  st.write(f'Selecione exatamente {size_5} países!')
else:
  data = shootouts_df[
    (shootouts_df['home_team'].isin(_countries)) |
    (shootouts_df['away_team'].isin(_countries))
  ]

  for _country in _countries:
    home = data['home_team'] == _country
    visitor = data['away_team'] == _country
    winner = data['winner'] == _country

    wins_home = len(data[(home) & (winner)])
    lose_home = len(data[(home) & -(winner)])
    
    wins_visitor = len(data[(visitor) & (winner)])
    lose_visitor = len(data[(visitor) & -(winner)])

    matches = wins_home + lose_home + wins_visitor + lose_visitor

    if matches != 0:
      st.write(f'{_country} jogou decisões por pênalti {matches} vezes.')
      st.write(f'Vitórias: {wins_home + wins_visitor}')
      st.write(f'Derrotas: {lose_home + lose_visitor}')

    if wins_home == 0 or wins_visitor == 0 or lose_home == 0 or lose_visitor == 0:
      st.write(f'{_country} não possui dados o suficiente para gerar um gráfico.')
      continue
    
    fig, ax = plt.subplots()
    ax.pie([wins_home, lose_home, wins_visitor, lose_visitor], 
        labels=['Vitórias em Casa', 'Derrotas em Casa', 'Vitórias como Visitante', 'Derrotas como Visitante']
    )
    ax.axis('equal')
    st.pyplot(fig)

with open('archive.zip', "rb") as f:
    st.download_button(
        label="Baixar Datasets",
        data=f,
        file_name='datasets.zip',
        mime="application/zip"
    )