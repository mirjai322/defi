import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

filename = "centralized_high_output/detail_data_iteration37.csv"
df_final = pd.DataFrame()

df0 = pd.read_csv(filename)
df = df0[df0["type"] == "agent"]
df = df[(df["iteration"] ==1)]
df['quartile'] = pd.qcut(df['money'], q=4, labels=False) + 1
grouped = df.groupby('quartile').size()
print(grouped)
df = pd.DataFrame(grouped)
df = df.rename(columns={df.columns[0]: 'Count'})
df['iteration'] = '1'
print (df)
df_final = pd.concat([df_final,df], axis=0)

df = df0[df0["type"] == "agent"]
df = df[(df["iteration"] ==500)]
print(df)
df['quartile'] = pd.qcut(df['money'], q=4, labels=False) + 1
grouped = df.groupby('quartile').size()
print(grouped)
df = pd.DataFrame(grouped)
df = df.rename(columns={df.columns[0]: 'Count'})
df['iteration'] = '500'
print(df)
df_final = pd.concat([df_final,df], axis=0)
print("****")
print(df_final)







