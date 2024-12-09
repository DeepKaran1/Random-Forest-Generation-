import random
from math import comb
import networkx as nx
import matplotlib.pyplot as plt

# Precompute t[n] and t_d[n][d] for tree generation
def compute_t_and_td(n_max):
    t = [0 for i in range(0, n_max + 1)]
    tdn = [[0 for d in range(0, n_max)] for n in range(0, n_max + 1)]
    t[1] = 1  # Base case: Only one tree with a single node
    for n in range(2, n_max + 1):
        tdn[n][1] = t[n - 1] * (n - 1)
        for d in range(2, n):
            tdn[n][d] = sum(
                comb(n - 2, i - 1) * tdn[n - i][d - 1] * t[i] * i
                for i in range(1, n - d + 1)
            )
        t[n] = sum(tdn[n][d] for d in range(1, n))
    return t, tdn

# Precompute f[n] and fc[n][c] for forest generation
def compute_f_and_fc(n_max):
    t = compute_t_and_td(n_max)[0]
    f = [0 for i in range(0, n_max + 1)]
    fcn = [[0 for c in range(0, n_max + 1)] for n in range(0, n_max + 1)]
    for n in range(1, n_max + 1):
        fcn[n][1] = t[n]
        for c in range(2, n + 1):
            fcn[n][c] = sum(
                comb(n - 1, i - 1) * fcn[n - i][c - 1] * t[i]
                for i in range(1, n - c + 2)
            )
        f[n] = sum(fcn[n][c] for c in range(1, n + 1))
    return f, fcn

# Generate a random labeled forest
def random_labeled_forest(n, S):
    global f, fcn
    if n <= 0:
        return []
    weights = [fcn[n][c] / f[n] for c in range(1, n + 1)]
    c = weighted_choice(weights) + 1
    return random_labeled_forest_c(n, c, S)

# Generate a random labeled forest with `c` components
def random_labeled_forest_c(n, c, S):
    global fcn
    if not S:  # Safeguard for empty set
        return []

    if c == 1:  # Base case: Single tree
        return labeled_tree(n, S)

    probabilities = [
        comb(n - 1, i - 1) * fcn[n - i][c - 1] * t[i] / fcn[n][c]
        for i in range(1, n - c + 2)
    ]
    probabilities = [p for p in probabilities if p > 0]  # Filter valid probabilities

    if not probabilities:  # If all probabilities are zero, stop recursion
        return []

    i = weighted_choice(probabilities) + 1

    # Ensure subset size is valid
    if i > len(S):
        i = len(S)

    Sw = set(random.sample(S, i))  # Randomly sample `i` elements
    Sdash = S - Sw

    # Recursive calls
    T1 = labeled_tree(i, Sw) if Sw else []
    F = random_labeled_forest_c(n - i, c - 1, Sdash) if Sdash else []

    return T1 + F

# Generate a labeled tree
def labeled_tree(n, S):
    if n == 1:
        # Return no edges for n=1; the node will be handled as an isolated point
        return []
    weights = [tdn[n][d] / t[n] for d in range(1, n)]
    d = weighted_choice(weights) + 1
    return labeled_tree_withd(n, d, S)

# Generate a labeled tree with depth `d`
def labeled_tree_withd(n, d, S):
    global t, tdn
    if not S:  # Safeguard for empty set
        return []

    x = min(S)  # Safely select the smallest element
    Sd = S - {x}  # Remove the selected root

    if d == 1:  # Base case: Star tree (depth = 1)
        return [(x, v) for v in Sd]

    # Compute probabilities for subtree sizes
    probabilities = [
        comb(len(S) - 2, i - 1) * tdn[len(S) - i][d - 1] * t[i] * i / tdn[len(S)][d]
        for i in range(1, len(S) - d + 1)
    ]
    probabilities = [p for p in probabilities if p > 0]  # Filter valid probabilities

    if not probabilities:  # If all probabilities are zero, stop recursion
        return []

    i = weighted_choice(probabilities) + 1

    # Ensure subset size is valid
    if i > len(Sd):
        i = len(Sd)

    subset = set(random.sample(Sd, i))  # Randomly sample `i` elements
    Sdash = Sd - subset

    # Recursive calls
    T1 = labeled_tree(i, subset) if subset else []
    T2 = labeled_tree_withd(n - i, d - 1, Sdash) if Sdash else []
    
    return T1 + T2 + [(x, min(subset))] if subset else T1 + T2

# Weighted choice for probabilities
def weighted_choice(weights):
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for i, weight in enumerate(weights):
        cumulative += weight
        if r < cumulative:
            return i
    return len(weights) - 1

# Visualize the forest
def visualize_tree(edges, n, S):
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Add isolated nodes explicitly
    all_nodes = {u for u, v in edges} | {v for u, v in edges}
    for node in S:
        if node not in all_nodes:
            G.add_node(node)
    
    if len(G.nodes) == 0:
        print("Tree generation failed. The tree is empty.")
        return
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos, with_labels=True, node_size=500, node_color="skyblue",
        font_size=10, font_weight="bold", edge_color="gray"
    )
    plt.title("Random Labeled Forest")
    plt.show()

# Main Execution
n = 25  # Number of vertices
S = set(range(1, n + 1))
t, tdn = compute_t_and_td(n)
f, fcn = compute_f_and_fc(n)

forest_edges = random_labeled_forest(n, S)
print("Generated Forest Edges:", forest_edges)
visualize_tree(forest_edges, n, S)
