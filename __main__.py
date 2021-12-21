import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from rich import print
import seaborn as sns
from sklearn.ensemble import IsolationForest

df = pd.read_csv("./ACME_dataset.csv", delimiter=";", index_col="project")
sns.set_style("darkgrid")


acme_df = df[df["approach"] == "ACME"]
axa_df = df[df["approach"] == "AXADEFEITO"]
acme_small_df = acme_df[acme_df["size"] == "Pequeno"]
acme_large_df = acme_df[acme_df["size"] == "Grande"]

df_small = df[df["size"] == "Pequeno"]
df_large = df[df["size"] == "Grande"]

axa_small_df = axa_df[axa_df["size"] == "Pequeno"]
axa_large_df = axa_df[axa_df["size"] == "Grande"]

df_small = df_small[
    (df_small["productivity"] < df_small["productivity"].quantile(0.95))
    & (df_small["productivity"] > df_small["productivity"].quantile(0.05))
]


df_large = df_large[
    (df_large["productivity"] < df_large["productivity"].quantile(0.95))
    & (df_large["productivity"] > df_large["productivity"].quantile(0.05))
]


print(acme_df.describe().to_markdown())
print(acme_df.median().to_markdown())
print(axa_df.describe().to_markdown())
print(axa_df.median().to_markdown())


hist = sns.histplot(df["productivity"])
hist.set_title("Productivity Frequency Distribution (General)")
plt.savefig("figures/hist.png")

rel_small = sns.relplot(x="kloc", y="productivity", data=df_small, hue="approach")
rel_small.fig.suptitle("Productivity by KLOC (small projects)")
plt.savefig("figures/rel_small.png")

rel_large = sns.relplot(x="kloc", y="productivity", data=df_large, hue="approach")
rel_large.fig.suptitle("Productivity by KLOC (large projects)")
plt.savefig("figures/rel_large.png")
plt.clf()

corr_axa = sns.heatmap(axa_df.corr())
corr_axa.set_title("Correlations (AXADEFEITO)", y=-0.12)
plt.savefig("figures/corr_axa.png")

corr_acme = sns.heatmap(acme_df.corr())
corr_acme.set_title("Correlations (ACME)", y=-0.12)

plt.savefig("figures/corr_acme.png")

plt.clf()

boxplot_small = sns.boxplot(x="approach", y="productivity", data=df_small)
boxplot_small.set_title("Productivity (Small Projects)")
plt.savefig("figures/boxplot_small.png")

plt.clf()
boxplot_large = sns.boxplot(x="approach", y="productivity", data=df_large)
boxplot_large.set_title("Productivity (Large Projects)")

plt.savefig("figures/boxplot_large.png")

iso = IsolationForest(contamination=0.1)
x = iso.fit_predict(df["productivity"].reshape(-1, 1))
print(x)
