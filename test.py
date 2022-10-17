import os
import pandas as pd
import csv


all_files = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/TAQ/daily_data_merged"
all_files2 = r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\robintrack\filtered_data"

# create here a list of files you want to merge into the an Excel file
files = [all_files2 + "/" + company for company in os.listdir(all_files)]
sheet_names = os.listdir(all_files)
print(files)

writer = pd.ExcelWriter('out2.xlsx', engine='xlsxwriter')

for i, file in enumerate(files):
    df = pd.read_csv(file, sep=",")

    df.to_excel(writer, sheet_name=str(sheet_names[i]))

writer.save()