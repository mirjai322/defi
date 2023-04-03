import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob as glob

def generate_consolidated_csv(a,b):
    paths = glob.glob(a+"_"+b+"_output/detail_data_iteration*.csv")
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    df = pd.concat(dfs,axis=0)
    df.to_csv(a+"_"+b+"_output/consolidated.csv", index=False)

consolidate = True
#hue_by = "id"
hue_by = "type"
if consolidate:
    generate_consolidated_csv("centralized","low")
    generate_consolidated_csv("centralized","medium")
    generate_consolidated_csv("centralized","high")
    generate_consolidated_csv("decentralized","low")
    generate_consolidated_csv("decentralized","medium")
    generate_consolidated_csv("decentralized","high")
    fname = "consolidated.csv"
else:
    fname = "detail_data_iteration0.csv"



############################################################################
#Figure 1: Pick a random run and show how agent networth changes per week
############################################################################

figure, subplot = plt.subplots(nrows=2, ncols=3, figsize=(12, 8),sharey=True)

# Plot something in each subplot
filename = "centralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[0,0])
subplot[0, 0].set_title('[Centralized-Low]')


filename = "centralized_medium_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[0,1])
subplot[0, 1].set_title('[Centralized-Medium]')

filename = "centralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[0,2])
subplot[0, 2].set_title('[Centralized-High]')

filename = "decentralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[1,0])
subplot[1, 0].set_title('[Decentralized-Low]')

filename = "decentralized_medium_output/" + fname
df = pd.read_csv(filename)
df.round(2)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[1,1])
subplot[1, 1].set_title('[Deentralized-Medium]')

filename = "decentralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue="subtype", data=df_agent, ax=subplot[1,2])
subplot[1, 2].set_title('[Decentralized-High]')

# Add a main title for the entire figure
figure.suptitle("Agents networth changes in a particular run")


############################################################################
#Figure 2: Pick the same random as above run and show how firm networth changes per week
############################################################################

figure, subplot = plt.subplots(nrows=2, ncols=3, figsize=(12, 8),sharey=True)

# Plot something in each subplot
filename = "centralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,0])
subplot[0, 0].set_title('[Centralized-Low]')


filename = "centralized_medium_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,1])
subplot[0, 1].set_title('[Centralized-Medium]')

filename = "centralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,2])
subplot[0, 2].set_title('[Centralized-High]')

filename = "decentralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,0])
subplot[1, 0].set_title('[Decentralized-Low]')

filename = "decentralized_medium_output/" + fname
df = pd.read_csv(filename)
df.round(2)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,1])
subplot[1, 1].set_title('[Deentralized-Medium]')

filename = "decentralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "firm"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,2])
subplot[1, 2].set_title('[Decentralized-High]')

# Add a main title for the entire figure
figure.suptitle("Firms networth changes in a particular run")


############################################################################
#Figure 3: Pick the same random run and show how regulator networth changes per week
############################################################################

figure, subplot = plt.subplots(nrows=2, ncols=3, figsize=(12, 8),sharey=True)

# Plot something in each subplot
filename = "centralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,0])
subplot[0, 0].set_title('[Centralized-Low]')


filename = "centralized_medium_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,1])
subplot[0, 1].set_title('[Centralized-Medium]')

filename = "centralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,2])
subplot[0, 2].set_title('[Centralized-High]')

filename = "decentralized_low_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,0])
subplot[1, 0].set_title('[Decentralized-Low]')

filename = "decentralized_medium_output/" + fname
df = pd.read_csv(filename)
df.round(2)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,1])
subplot[1, 1].set_title('[Deentralized-Medium]')

filename = "decentralized_high_output/" + fname
df = pd.read_csv(filename)
df_agent = df[df["type"] == "regulator"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,2])
subplot[1, 2].set_title('[Decentralized-High]')

# Add a main title for the entire figure
figure.suptitle("Regulators networth changes in a particular run")


############################################################################
# Figure 4: stddev under different runs
############################################################################

figure, subplot = plt.subplots(nrows=2, ncols=3, figsize=(12, 8),sharey=True)

# Plot something in each subplot
filename = "centralized_low_output/summary.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
subplot[0, 0].plot(df_agent['run'], df_agent['stddev'])
subplot[0, 0].set_title('[Centralized-Low]')


filename = "centralized_medium_output/summary.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
subplot[0, 1].plot(df_agent['run'], df_agent['stddev'])
subplot[0, 1].set_title('[Centralized-Medium]')

filename = "centralized_high_output/summary.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
subplot[0, 2].plot(df_agent['run'], df_agent['stddev'])
subplot[0, 2].set_title('[Centralized-High]')

filename = "decentralized_low_output/summary.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
subplot[1, 0].plot(df_agent['run'], df_agent['stddev'])
subplot[1, 0].set_title('[Decentralized-Low]')

filename = "decentralized_medium_output/summary.csv"
df = pd.read_csv(filename)
df.round(2)
df_agent = df[df["type"] == "agent"]
subplot[1, 1].plot(df_agent['run'], df_agent['stddev'])
subplot[1, 1].set_title('[Deentralized-Medium]')

filename = "decentralized_high_output/summary.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
subplot[1, 2].plot(df_agent['run'], df_agent['stddev'])
subplot[1, 2].set_title('[Decentralized-High]')

# Add a main title for the entire figure
figure.suptitle('Standard Deviation of Agent Networth')

"""
############################################################################
# Figure 3: how did poor , middle and rich do at the end?
# group agents into poor, middle and rich
# plot number of poors, middle and rich at every 100 weeks or at start and then at end?
# 3 bar charts at beginning , end and may be after every 100
############################################################################

figure, subplot = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

# Plot something in each subplot
filename = "centralized_low_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,0])
subplot[0, 0].set_title('[Centralized-Low]')


filename = "centralized_medium_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,1])
subplot[0, 1].set_title('[Centralized-Medium]')

filename = "centralized_high_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[0,2])
subplot[0, 2].set_title('[Centralized-High]')

filename = "decentralized_low_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,0])
subplot[1, 0].set_title('[Decentralized-Low]')

filename = "decentralized_medium_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df.round(2)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,1])
subplot[1, 1].set_title('[Deentralized-Medium]')

filename = "decentralized_high_output/detail_data_iteration37.csv"
df = pd.read_csv(filename)
df_agent = df[df["type"] == "agent"]
sns.lineplot(x="iteration", y="money", hue=hue_by, data=df_agent, ax=subplot[1,2])
subplot[1, 2].set_title('[Decentralized-High]')

# Add a main title for the entire figure
figure.suptitle("Agents networth changes in a particular run")




"""
plt.show()
