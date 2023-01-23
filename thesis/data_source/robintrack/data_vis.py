import pandas as pd
import matplotlib.pyplot as plt
from thesis import tools

pd.set_option('display.max_rows', 500)

data = tools.JsonEditor.read_from_json(r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\results\summary2.json")
# data2 = tools.JsonEditor.read_from_json(r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\results\stdev.json")

# Show average holders per bin
df = pd.DataFrame.from_dict(data, orient='index', columns=['average_holders', 'variance', 'nvar'])
# plt.hist(df['average_holders'], bins=[0, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000])
df["bins"] = pd.cut(df['average_holders'], [0,500,2500,12500,60000])
# df["bins"] = pd.cut(df['average_holders'], [0,5000,10000,50000])

# df["bins"].value_counts().plot.bar()
# plt.xlabel('number of holders')
# plt.ylabel('number of firms')
# plt.title("avg_holder distribution")
# plt.xticks(rotation=0)
#
# plt.show()

# Remove stocks with less than 100 holders
df = df[df['average_holders'] > 100]

# Removing outliers
df['normalised'] = df['variance']/df['average_holders']
df = df[df['normalised'] < df['normalised'].quantile(0.99)]
df = df[df['normalised'] > df['normalised'].quantile(0.01)]


print(df)
print(df['average_holders'].nlargest(10))
exit()
# print(df.nlargest(200, 'normalised'))
# print(df['normalised'].mean())


# plt.scatter(df['variance'], df['average_holders'])
# plt.show()
# plt.scatter(df['nvar'], df['average_holders'])
# plt.show()
plt.xlabel('variance / number of holders')
plt.ylabel('number of holders')
plt.title("variance - holder plotted")
plt.scatter(df['normalised'], df['average_holders'])
plt.show()
# df.plot.hist(bins=10, logx=True)
# df.average_holders.plot(kind='kde')
# df.plot(kind='hist')

