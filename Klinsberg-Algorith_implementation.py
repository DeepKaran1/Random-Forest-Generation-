

import networkx as nx
import matplotlib.pyplot as plt

#
def construct_tree(a):
    n = len(a) + 2  #a is the input Prufer sequence of length n-2 
    print("n=", n) 
    #redefine a
    a.append(n-1) # a_{n-1} <- n in NW; changed to a_{n-2} <- n-1 because of 
    print("extended a=", a)
    tree = [0] * n #Initialize tree with 0 - this is correct
    print("tree=", tree)

    k = 0 #k >= k'; k' always points to the minimum index that is "eligible" (=0)
    j = 0 # this is used as index for the prufer sequence

    #a.append(n-1)  # Set a[n-2] to n - 1 : why ?
    #print(a) #this is correct

    # Step A: Initialize
    #print("n-3=", n-3)
    for i in range(n - 3, -1, -1):  # Iterate from n-3 to 0, corresponds to n-2 to 1; see stanford page for definitions of range
        if tree[a[i]] == -1:
            continue
        tree[a[i]] = -1
        a[i] = -a[i]
    #checking
    print("tree = ", tree)
    print("pf sequence=", a)
   
    #Step (B)
    def resetk(k):
        print("current tree entries =", tree)
        l = k
        while( l < n-1 and tree[l] != 0):
            l = l+1
        return l
    k = resetk(k) 
    kPrime = k #kPrime <= k always
    #checking
    print ("k, kPrime =", k, kPrime)  #check

    # Steps C
    edge_list = []
    while j < n - 1:   #this bound is correct - we add n-1 edges 
        # Step C: Enter next edge
        r = abs(a[j])
        tree[kPrime] = r
        edge_list.append((kPrime, r)) #new edge

        if (a[j] >= 0):  #reset k and k', allowing for 0 in the Prufer sequence; this ca n be a[j] > 0 if 0 is disallowed 
            k  = resetk(k)
            kPrime = k
        else:
            print("a[j] =", a[j]) #check
            if (r > k):
                tree[r] = 0
                k  = resetk(k)
                kPrime = k
                print ("k, kPrime =", k, kPrime)  #check
            else:
                kPrime = r
                print("kPrime =", kPrime) #now kPrime < k
        j = j + 1  #correct place to increment j for next edge
    return edge_list

def visualize_tree_construction(a):
    tree_edges = construct_tree(a)
    print(tree_edges)
    G = nx.Graph()

    for i, edge in enumerate(tree_edges, 1):
        G.add_edge(*edge)
        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, font_size=20)
        plt.title(f"Graph after adding edge: {edge}")
        plt.show()  # This will wait until the window is closed before continuing to the next iteration


a = [5, 4, 5, 2, 3, 2, 6]  # Example input sequence, with values in the range 0 to 7; can't include a 0 in the label set 

visualize_tree_construction(a)
