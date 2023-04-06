import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

sushi_pools = pd.read_csv("sushi_pairs.csv")
uniq_sushi_pools = set(sushi_pools.id)  # same len as without set
sushi_pools_creators = pd.read_csv("sushi_pool_creators.csv")
sushi_pools_creators = sushi_pools_creators.iloc[:, 1:]


sushi_pools_creators.columns = ["id", "creator_address", "creation_txn"]
uniq_sushi_creators = set(sushi_pools_creators.creator_address)
sushi_pools = sushi_pools.merge(sushi_pools_creators, on="id")

poolsV3 = pd.read_csv("rawPools_V3.csv")
pool_creators = pd.read_csv("pool_creators.csv")
pool_creators = pool_creators.iloc[:, 1:]
pool_creators.columns = ["id", "creator_address", "creation_txn"]
poolsV3 = poolsV3.merge(pool_creators, on="id")

combined = pd.read_csv("pools_sushi_uni_wCreators.csv")


G = nx.from_pandas_edgelist(
    combined, source="creator_address", target="id")


colors = []

for node in G:
    if node in combined["creator_address"].values:
        colors.append("blue")
    else:
        if node in poolsV3["id"].values:
            colors.append("pink")
        else:
            colors.append("purple")


nx.draw(G, pos=nx.spring_layout(G), node_size=10,
        node_color=colors, with_labels=False)
plt.show()
