import numpy as np
    
def find_lowest(OPEN = None): 
    #This function order the OPEN list from the node with the lowest F value to
#the node with the longest F value
    
    __,co = OPEN.shape
    L = []
    __,cl = L.shape
    lowest = 1
    while (cl < co):

        for j in np.arange(1,co+1).reshape(-1):
            if (OPEN(j).f != np.inf):
                node = OPEN(j)
                lowest = j
                break
        for i in np.arange(1,co+1).reshape(-1):
            if (OPEN(i).f != np.inf):
                if (OPEN(i).f < node.f):
                    node = OPEN(i)
                    lowest = i
        OPEN(lowest).f = np.inf
        L = np.array([L,node])
        __,cl = L.shape
        node = np.inf

    
    node = L(1)
    
    return node,L
    
    return node,L