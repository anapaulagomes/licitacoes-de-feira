import pandas as pd
import sqlite3

connection = sqlite3.connect("payments.sqlite")


payments = pd.read_csv("../data/payments/all_payments-2010-01-01-2019-03-14.csv")
payments.to_sql("payments", con=connection)
