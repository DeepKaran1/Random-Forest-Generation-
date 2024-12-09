
import random
from math import comb  
import networkx as nx  
import matplotlib.pyplot as plt  


def compute_t_and_td(n_max):
  
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

    return t, tdn  # Return the computed tables


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
   
    Sdash = subset
    #print("subset=", subset)
    T1 = list(labeled_tree(i,Sdash))
    print("T1=", T1)
    
    Sdash = S - subset
    T2 = list(labeled_tree_withd(n-i, d-1, Sdash))
    return T1 + T2 + [(x, min(subset))]

def labeled_tree(n, S):
    if (n == 1):
        return {}
    else:



        weights = [tdn[n][d]/t[n] for d in range(1, n)]  # Weights (probabilities) for degree selection, 1 <= d <= n-1
        print("weights=", weights)
   
        cumWeights = 0
        i = 0
        x = random.uniform(0, 1)
    #print("x =", x)
        while (x > cumWeights):
            cumWeights += weights[i]
            i += 1
        d = i
        print("d=", d) #this is now correct

   
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
