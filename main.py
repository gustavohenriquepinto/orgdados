import pandas

def print_head(data_frame : pandas.DataFrame, lines : int = 5) -> None:
  print(data_frame.head(lines), '\n')

results_data_frame : pandas.DataFrame = pandas.read_csv('results.csv')
goalscorers_data_frame : pandas.DataFrame = pandas.read_csv('goalscorers.csv')
shootouts_data_frame : pandas.DataFrame = pandas.read_csv('shootouts.csv')

print_head(results_data_frame)
print_head(goalscorers_data_frame)
print_head(shootouts_data_frame)
