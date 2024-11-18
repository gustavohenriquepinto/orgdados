import pandas as pd
import streamlit as st
import datetime
from dashboard import Dashboard

main = Dashboard()

main.read_datasets()
main.show_filters()
main.apply_filters()
main.show_dashboard()
