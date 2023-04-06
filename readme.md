### Data Files

Anything for sushiswap is labeled with "sushi", all else is Uniswap V3 (I know this is bad lol, I'm fixing it)

### Development Timeline

1. pool_creation_graph.ipynb

2. temporal_pool_graphs.ipynb

3. liquidity_pool_transport_small.ipynb
   Testing out Fused Gromov-Wasserstein transport method on a subgraph of the sushiswap exchange.
   This uses an old structure where users connect to liquidity pools that they've interacted with, however FGW doesn't work (well) with disconnected graphs.
   Feature here was only if it is a liqudity pool or a user.

4. liquidity_pool_transport_struct2.ipynb

   This implements the FGW transport method on a new graph structure where users are connected to tokens that they have interacted with through a liqudity pool.
   Freatures here are

   - \[num neighbors, num_liq_snaps, num_pools_created, avg_snaps/pool\]
   - \[num neighbors, -1, -1, -1\]
     (Needs to be enhanced for later applications)

5. liquidity_pool_transport_struct1.ipynb

   In this graph implementation, users are connected to Liquidity pools which are then connected to tokens.
   Freatures here are (same as above)

   - \[num neighbors, num_liq_snaps, num_pools_created, -1, avg_snaps/pool\]
   - \[num neighbors, -1, -1, TVL, -1\]

   (Note for 4 and 5, if using a large graph, then use
   `pi, log =ot.gromov.fused_gromov_wasserstein(M, C1, C2, t1masses, t2masses, alpha=alpha, log=True))`
