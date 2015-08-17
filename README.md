# Experiment with mesh clustering

Approach: fix max load/processor and solve for minimum communication cost

p_i = processor assignment for vertex
w_i = size of grid i
T = maximum grid weight
e_{i,k} edge weight

Communication cost:

\sum_{i,k \in E} e_{i,k} d_{i,k}

Minimize communication cost for fixed T

\min \sum_{i,k \in E} e_{i,k} d_{i,k}

\forall i,k \in E : \sum_j p_{i,j} - p_{k,j} - d_{i,k} <= 0
\forall i,k \in E : -d_{i,k} >= 0
\forall j \in P : \sum_{i \in V} p_{i,j} w_i <= T
\forall i \in V : \sum_{j \in P} p_{i,j} = 1
\forall i \in V, j \in P : -p_{i,j} <= 0

NP-hard: require p_{i,j} is integer

Reduces to k-coloring
