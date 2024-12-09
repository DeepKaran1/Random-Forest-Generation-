#AM - got it working finally on 20 Oct, 2024
import random
from math import comb  
import networkx as nx  
import matplotlib.pyplot as plt  

# Precompute tables for t(n) and t_d(n) using recursive relations
# This works correctly
def compute_t_and_td(n_max):
    #############################################
    # In t[n][d], d is the column index and n the row index
    # Interestingly, all indexing starts from 0;
    # the ranges are just used to determine the number of rows and columns
    # get t[n][d] for 2 <= n <= n_max and 1 <= d <= n_max-1
    ##############################################
    # Initialize the t and tdn tables with zeroes
    t = [0 for i in range(0, n_max + 1)]  # don't care about t[0] but the values for t[1], t[2], ..., t[n_max]
    print("t is:", t)
    tdn = [[0 for d in range(0, n_max)] for n in range(0, n_max + 1)]
    print("t[n][d] array is:", tdn)

    # Base case
    t[1] = 1  # There's only one tree of size 1 (a single node)
    # Compute t_d(n) for each degree d for n >= 2, d >= 1
    for n in range(2, n_max + 1): # n <= 2 <= n_max
        tdn[n][1] = t[n-1]*(n-1) # for d = 1 and n >= 2
        for d in range(2, n):  # 2 <= d <= n-1
            tdn[n][d] = sum(comb(n - 2, i - 1) * tdn[n-i][d-1] * t[i] * i
            for i in range(1, n - d+1)
            )
        t[n] = sum(tdn[n][d] for d in range(1, n))
    #print("The array t[n] is:", t) # now i am getting correct output
    #print("The table t[d][n] is:", tdn) # now i am getting correct output
    return t, tdn  # Return the computed tables

# Recursive function to construct a labeled tree based on the algorithm
#def labeled_tree(n, d, S, parent=None):
def labeled_tree_withd(n, d, S):
    global t, tdn
    x = min(S)
    Sd = S - {min(S)} # min(S) is to get the vertex with smallest label in S
    if (d == 1):
        v = random.choice(list(Sd)) # a set must be made into a list for this random choice to work
        T = [(min(S), v)] # add this edge to T
        T = T + list(labeled_tree(n-1, Sd)) # and all the other edges; turning the return type into a list type
        return T
    else: # d >= 2; choose the size of the split tree
        # print(tdn)
        probabilities = [
        #(comb(len(Sd) - 1, i - 1) *  tdn[i][d-1] * t[len(Sd) - i - 1] * i)
         (comb(len(S) - 2, i - 1) * tdn[len(S) - i][d - 1] * t[i] * i)/tdn[len(S)][d]
         for i in range(1, len(S) - d +1)
        ]
    print("The probabilities are:", probabilities)
    total = sum(probabilities)  # Sum of all probabilities
    print("total =", total)

    # If total probability is 0 (rare case, when and why ?), choose i randomly; otherwise, sample using weights
    if total == 0:
        i = 1 if len(Sd) == 1 else random.randint(1, len(Sd) - 1)
    else:
        # probabilities are already normalized
        # Normalize the probabilities and select i using weighted random choice
        # probabilities = [p / total for p in probabilities]
        #i = random.choices(range(1, len(Sd)), weights=probabilities)[0]

        cumProbabilities = 0
        j = 0
        y = random.uniform(0, 1)
        print("y =", y)
        while (y > cumProbabilities):
            cumProbabilities += probabilities[j]
            j += 1
        i = j
        print("i=", i)  # this is now correct
    # Select a random subset of size i from the remaining nodes
    Sd_list = list(Sd)  # Convert set to list for sampling
    subset = set(random.sample(Sd_list, i))  # Randomly select i nodes
    #Sdd = Sd - subset  # Remaining nodes after selection
    #Sdash = set(range(1, i+1))
    #Sdash = subset
    Sdash = subset
    #print("subset=", subset)
    T1 = list(labeled_tree(i,Sdash))
    print("T1=", T1)
    #relabel vertices in Sdash with labels of the randomly chosen subset
    # Recursively construct the subtrees
    #T1 = labeled_tree(n-i, d - 1, subset x)  # First subtree ?
    #T2 = labeled_tree(len(Sd_dash) + 1, d, Sd_dash | {x}, t, tdn, parent)  # Second subtree ?
    Sdash = S - subset
    T2 = list(labeled_tree_withd(n-i, d-1, Sdash))
    return T1 + T2 + [(x, min(subset))]

    # Combine the two subtrees and return the edges
    #eturn T1 + T2

# Generate a random labeled tree of size n
# fixed this
def labeled_tree(n, S):
    if (n == 1):
        return {}
    else:

    #global t, tdn
    # Precompute the t(n) and t_d(n) tables for the given size n
    #t, tdn = compute_t_and_td(n)
    # print(t) #for n=5, it is printing 0, 1, 1, 1, 1, 1, which is wrong; fixed this
    # print(tdn) #fixed this, too

    # Initialize the set of all nodes from 1 to n
    #move this to main
    #S = set(range(1, n + 1))

    # Select a degree d with probability proportional to t_d(d, n)
    # 1 <= d <= n-1. this means n >= 2
    # tdn[1][1] is not defined
    # tdn[1][2] = t[1] = 1
        weights = [tdn[n][d]/t[n] for d in range(1, n)]  # Weights (probabilities) for degree selection, 1 <= d <= n-1
        print("weights=", weights)
    #print(weights[0])
    #weights = [td[d][n]/t[n] for d in range(1, n)] #these weights are probabilities
    #d = random.choices(range(1, n + 1), weights=weights)[0] if sum(weights) else random.randint(1, n) #??
        cumWeights = 0
        i = 0
        x = random.uniform(0, 1)
    #print("x =", x)
        while (x > cumWeights):
            cumWeights += weights[i]
            i += 1
        d = i
        print("d=", d) #this is now correct

    # Generate and return the edges of the tree
    # return labeled_tree(n, d, S, t, tdn)
        return labeled_tree_withd(n, d, S) # what is the fourth argument of this call ?

#this function is fine
def visualize_tree(edges):
  
    G = nx.Graph()
    G.add_edges_from(edges)  

    if len(G.nodes) == 0:
        print("Tree generation failed. The tree is empty.")
        return

    
    pos = nx.spring_layout(G)  
   
    plt.figure(figsize=(8, 6))  
    nx.draw(
        G, pos, with_labels=True, node_size=500, node_color='skyblue',
        font_size=10, font_weight='bold', edge_color='gray'
    )
    plt.title("Random Labeled Tree")  
    plt.show()  

#get n as user-input
n = 7 #Number of vertices
S = set(range(1, n + 1)) #this is an example of a set constructor
print("The set is:", S)
# compute the tables tdn and t here
global t, tdn
t, tdn = compute_t_and_td(n) # these are global lists  available at all levels of recursion
edges = labeled_tree(n, S)
print(type(edges))
print("Generated Tree Edges:", edges)  
visualize_tree(edges)  
