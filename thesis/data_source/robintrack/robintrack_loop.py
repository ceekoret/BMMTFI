import os
import pandas as pd
from thesis import tools

pd.set_option('display.max_rows', 1000)

path = r"C:\Users\Ck0rt\Documents\Large files\School\MSc Finance & Investments\Thesis\Robintrack\popularity_export"


def loop_robintrack(results_path):
    results_dict = {}

    for filename in os.listdir(path):
        csv_path = os.path.join(path, filename)

        # checking if it is a file
        if os.path.isfile(csv_path):
            # print(csv_path)

            df = pd.read_csv(csv_path)
            # print(df.iloc[-20:])
            # print(df['users_holding'].iloc[-20:])
            # Calculate the mean number of holders of this share in the last month
            try:
                # value = df['users_holding'].std()
                # value = round(value)
                final_holder_count = df['users_holding'].iloc[-20:].mean()
                final_holder_count = round(final_holder_count)
                df['variance'] = df['users_holding'].rolling(5).var()
                df['mean'] = df['users_holding'].rolling(5).mean()
                df['norm_var'] = df['variance'] / df['mean']
                # print(df.iloc[100:260])
                variance = df['variance'].mean()
                variance = round(variance, 1)
                norm_var = df['norm_var'].mean()
                norm_var = round(norm_var, 6)

            except Exception as e:
                print(f"No value found: {e}")
                final_holder_count = 0
                norm_var = 0
            results_dict[filename] = [final_holder_count, variance, norm_var]
            print(f"Stock [{filename}] has an average of [{final_holder_count}] holders in the last month. Variance = {variance} - Nvar {norm_var}")

    tools.JsonEditor.write_to_json(results_path, results_dict)

loop_robintrack(results_path=r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\results\summary2.json")