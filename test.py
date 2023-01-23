import os
import pandas as pd
import csv

filedir = r"C:\Users\Ck0rt\Documents\Large files\School\MSc Finance & Investments\Thesis\Robintrack\popularity_export"

bin_500 = 0
bin_1000 = 0
bin_10000 = 0
bin_100000 = 0
bin_plus = 0


for filename in os.listdir(filedir):
    csv_path = os.path.join(filedir, filename)

    # checking if it is a file
    if os.path.isfile(csv_path):
        print(f"Now analysing data for Robintrack file: {filename}")
        df = pd.read_csv(csv_path)

        average_users = df.users_holding.mean().round()

        if average_users <= 500:
            bin_500 += 1
        elif average_users <= 1000:
            bin_1000 += 1
        elif average_users <= 10000:
            bin_10000 += 1
        elif average_users <= 100000:
            bin_100000 += 1
        else:
            bin_plus += 1


print(f"Number of stocks in bin_500: {bin_500}")
print(f"Number of stocks in bin_1000: {bin_1000}")
print(f"Number of stocks in bin_10000: {bin_10000}")
print(f"Number of stocks in bin_100000: {bin_100000}")
print(f"Number of stocks in bin_plus: {bin_plus}")

exit()



# all_files = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/TAQ/daily_data_merged"
# all_files2 = r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\robintrack\filtered_data"
#
# # create here a list of files you want to merge into the an Excel file
# files = [all_files2 + "/" + company for company in os.listdir(all_files)]
# sheet_names = os.listdir(all_files)
# print(files)
#
# writer = pd.ExcelWriter('out2.xlsx', engine='xlsxwriter')
#
# for i, file in enumerate(files):
#     df = pd.read_csv(file, sep=",")
#
#     df.to_excel(writer, sheet_name=str(sheet_names[i]))
#
# writer.save()