import pandas
import streamlit

def data_frame_info(name : str, data_frame : pandas.DataFrame, lines : int = 5) -> None:
  print(name)
  data_frame.info()
  print(data_frame.head(lines))
  print()



results_data_frame : pandas.DataFrame = pandas.read_csv('results.csv')
goalscorers_data_frame : pandas.DataFrame = pandas.read_csv('goalscorers.csv')
shootouts_data_frame : pandas.DataFrame = pandas.read_csv('shootouts.csv')

data_frame_info("RESULTS", results_data_frame)
data_frame_info("GOAL SCORERS", goalscorers_data_frame)
data_frame_info("SHOOT OUTS", shootouts_data_frame)
