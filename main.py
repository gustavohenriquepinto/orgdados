import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def data_frame_info(name : str, data_frame : pd.DataFrame, lines : int = 5) -> None:
  print(name)

  # print(data_frame.isna().any())
  # print(data_frame.shape)
  # data_frame.info()
  # print(data_frame.describe())

  print(data_frame.head(lines))
  print()

results_data_frame : pd.DataFrame = pd.read_csv('results.csv')
goalscorers_data_frame : pd.DataFrame = pd.read_csv('goalscorers.csv')
shootouts_data_frame : pd.DataFrame = pd.read_csv('shootouts.csv')

data_frame_info("RESULTS", results_data_frame)
# data_frame_info("GOAL SCORERS", goalscorers_data_frame)
# data_frame_info("SHOOT OUTS", shootouts_data_frame)

results_grouped_by_country = results_data_frame.groupby('country').size()
# print(results_grouped_by_country)

plt.figure(figsize=(10, 6))
results_grouped_by_country.plot(kind='barh', color='skyblue')
plt.title('Matches amount by country')
plt.xlabel('Matches')
plt.ylabel('Country')
plt.show()