import torch
import numpy as np
import struct
# Importing the statistics module
import statistics
# Importing the statistics module
from statistics import mean
#from statistics import kmeans
from ismember import ismember
from kmeans_pytorch import kmeans
from ast import ClassDef



#funcion struct2table en python: convierte una estructura a una lista
def myStruct2table(list):
    #arr = np.array(estructura)
    try: 
       arr = np.array(list) 
    except:
       print('error en arr = np.array(estructura)')  
       arr = list 
    lst = []

    for x in arr:
        lst.append(x)
    return lst



    
def search_uav_operations(subpath = None,uav_data = None,cfgParams = None): 
    path = np.round(subpath,4)
    home = np.array([[path(1,1)],[path(2,1)]])
    stops = 0
    __,N = path.shape
    h = N - 1
    vertex_node = {'parent' : - 1,'x' : path(1,1),'y' : path(2,1),'t' : 0,'g' : 0,'h' : 0,'f' : 0,'r' : N - 1}
    vertex_node['h'] = computeH_LKH2(path,vertex_node,uav_data,cfgParams)
    vertex_node['f'] = vertex_node['h']
    sol_found = False
    expanded_nodes = 0
    dist = 0
    time = 0
    rte = []
    OPEN = vertex_node
    CLOSE = []
    while (not len(OPEN)==0 ):

        current_node,OPEN = find_lowest(OPEN)
        #Delete current_node from OPEN
        OPEN(1).f = np.inf   
        OPEN = deleteNode(OPEN)
        ##Goal Node is HOME with h=0
        if (isSamePoint(np.array([[current_node.x],[current_node.y]]),home) and current_node.r == 0):  #como acceder a los .y, .r
            sol_found = True
            break
        SUCS = expand_graph(current_node,path,vertex_node,uav_data,cfgParams)
        __,n_sucs = SUCS.shape
        for i in np.arange(1,n_sucs+1).reshape(-1):
            in_closed = is_visited(CLOSE,SUCS(i))
            if (0 == in_closed):
                in_open = is_visited(OPEN,SUCS(i))
                if (0 == in_open):
                    SUCS(i).t = + np.inf
                    SUCS(i).parent = ''
                    suc = SUCS(i)
                else:
                    suc = OPEN(in_open)
                #Get the suc replicant in OPEN
                OPEN = UpdateVertex(OPEN,current_node,suc,uav_data,vertex_node)
        expanded_nodes = expanded_nodes + n_sucs
        #[sanityCheck] = SanityCheck(OPEN);
#Put current_node in list of nodes currently visited CLOSED
        CLOSE = np.array([CLOSE,current_node])

    
    if (sol_found):
        rte,dist = reconstruct_path(current_node,rte,dist,path)
        __,c = rte.shape
        for i in np.arange(2,c - 1+1).reshape(-1):
            if (rte(i) == 1):
                stops = stops + 1
        time = current_node.t
    else:
        print('UAV Subpath solution NOT found!')
    
    return rte,dist,time,stops
    
    
def UpdateVertex(OPEN = None,current_node = None,suc = None,uav_data = None,vertex_node = None): 
    d = EUC_2D_Distance(np.array([[suc.x],[suc.y]]),np.array([[current_node.x],[current_node.y]]))
    t = EUC_2D_Time(d,uav_data)
    if (isSamePoint(np.array([[current_node.x],[current_node.y]]),np.array([[vertex_node['x']],[vertex_node['y']]]))):
        t = uav_data.To + t
    else:
        if (isSamePoint(np.array([[suc.x],[suc.y]]),np.array([[vertex_node['x']],[vertex_node['y']]]))):
            tc = uav_data.Tt - t
            t = t + uav_data.Tl + tc
    
    if (current_node.t + t < suc.t):
        suc.t = current_node.t + t
        suc.parent = current_node
        if (is_visited(OPEN,suc) > 0):
            OPEN = remove(OPEN,suc)
        suc.f = suc.t + suc.h
        OPEN = np.array([OPEN,suc])
    
    return OPEN
    
    
def remove(OPEN = None,node = None): 
    list = OPEN
    idx = 0
    if (not len(list)==0 ):
        list = myStruct2table(list)
        list = np.array([list[:,np.arange(2,3+1)],list[:,6],list[:,8]])
        node = myStruct2table(node)
        node = np.array([node[:,np.arange(2,3+1)],node[:,6],node[:,8]])
        r,__ = list.shape
        for i in np.arange(1,r+1).reshape(-1):
            if (list[i,:] == node[1,:]):
                idx = i
                break
        OPEN(idx).f = np.inf
        OPEN = deleteNode(OPEN)
    
    return OPEN
    
    
def is_visited(list = None,node = None): 
    nodeIdx = 0
    if (not len(list)==0 ):
        list = myStruct2table(list)
        list = np.array([list[:,np.arange(2,3+1)],list[:,6],list[:,8]])
        node = myStruct2table(node)
        node = np.array([node[:,np.arange(2,3+1)],node[:,6],node[:,8]])
        r,__ = list.shape
        for i in np.arange(1,r+1).reshape(-1):
            if (list[i,:] == node[1,:]):
                nodeIdx = i
                break
    
    return nodeIdx
    
    
def is_visited_Working(list = None,node = None): 
    in_list = 0
    if (not len(list)==0 ):
        list = myStruct2table(list)
        list = np.array([list[:,np.arange(2,3+1)],list[:,6]])
        node = myStruct2table(node)
        node = np.array([node[:,np.arange(2,3+1)],node[:,6]])
        in_list = sum(ismember(list,node,'rows')) >= 1
    
    return in_list
    
    
def isSamePath(nodeA = None,nodeB = None): 
    if (np.logical_and((ClassDef(nodeA) == 'struct'),(ClassDef(nodeB) == 'struct'))):
        if (isSamePoint(np.array([[nodeA.x],[nodeA.y]]),np.array([[nodeB.x],[nodeB.y]]))):
            sol = isSamePath(nodeA.parent,nodeB.parent)
        else:
            sol = False
    else:
        if (np.logical_and((ClassDef(nodeA) != 'struct'),(ClassDef(nodeB) != 'struct'))):
            if (isSamePoint(np.array([[nodeA.x],[nodeA.y]]),np.array([[nodeB.x],[nodeB.y]]))):
                sol = True
            else:
                sol = False
        else:
            sol = False
    
    return sol
    
    
def deleteNode(OPEN = None): 
    L = []
    __,c = OPEN.shape
    for i in np.arange(1,c+1).reshape(-1):
        if (OPEN(i).f != np.inf):
            L = np.array([L,OPEN(i)])
    
    OPEN = L
    return OPEN
    
    
def reconstruct_path(current_node = None,rte = None,d = None,path = None): 
    __,c = path.shape
    for i in np.arange(1,c+1).reshape(-1):
        if (isSamePoint(np.array([[current_node.x],[current_node.y]]),path[:,i])):
            rte = np.array([i,rte])
            if (ClassDef(current_node.parent) == 'struct'):
                d = d + EUC_2D_Distance(np.array([[current_node.x],[current_node.y]]),np.array([[current_node.parent.x],[current_node.parent.y]]))
                rte,d = reconstruct_path(current_node.parent,rte,d,path)
                break
    
    return rte,d
    
    
def find_lowest(OPEN = None): 
    #This function order the OPEN list from the node with the lowest F value to
#the node with the highest F value
    
    __,co = OPEN.shape
    L = []
    lowest = 1
    __,cl = L.shape
    while (cl < co):

        for j in np.arange(1,co+1).reshape(-1):
            if (OPEN(j).f != np.inf):
                node = OPEN(j)
                lowest = j
                break
        if (ClassDef(node) == 'struct'):
            for i in np.arange(1,co+1).reshape(-1):
                if (OPEN(i).f != np.inf):
                    if (OPEN(i).f < node.f):
                        node = OPEN(i)
                        lowest = i
            OPEN(lowest).f = np.inf
            L = np.array([L,node])
            node = np.inf
            __,cl = L.shape

    
    node = L(1)
    
    return node,L
    
    
def expand_graph(current_node = None,path = None,vertex_node = None,uav_data = None,cfgParams = None): 
    __,c = path.shape
    L = []
    for i in np.arange(1,c+1).reshape(-1):
        suc = np.array([[path(1,i)],[path(2,i)]])
        if (not isSamePoint(np.array([[current_node.x],[current_node.y]]),suc) ):
            if (isSamePoint(np.array([[vertex_node['x']],[vertex_node['y']]]),suc)):
                is_rel = False
            else:
                is_rel = is_inpath(current_node,suc)
            if (not is_rel ):
                d_toSuc = EUC_2D_Distance(np.array([[current_node['x']],[current_node['y']]]),suc)
                t_toSuc = EUC_2D_Time(d_toSuc,uav_data)
                if (isSamePoint(np.array([[current_node['x']],[current_node['y']]]),np.array([[vertex_node['x']],[vertex_node['y']]]))):
                    g = uav_data['To'] + t_toSuc
                    t_toSuc = current_node['t'] + uav_data['To'] + t_toSuc
                else:
                    g = current_node['g'] + t_toSuc
                    if (isSamePoint(suc,np.array([[vertex_node['x']],[vertex_node['y']]]))):
                        tc = uav_data['Tt'] - g
                        t_toSuc = current_node['t'] + t_toSuc + uav_data['Tl'] + tc
                    else:
                        t_toSuc = current_node['t'] + t_toSuc
                d_tohome = EUC_2D_Distance(np.array([[vertex_node['x']],[vertex_node['y']]]),suc)
                t_tohome = EUC_2D_Time(d_tohome,uav_data)
                if (uav_data['Tt'] >= int(np.floor(g + t_tohome + uav_data['Tl']))):
                    suc = {'parent' : current_node,'x' : suc(1,1),'y' : suc(2,1),'t' : t_toSuc,'g' : g,'h' : 0,'f' : 0,'r' : 0}
                    if (isSamePoint(np.array([[suc.x],[suc.y]]),np.array([[vertex_node['x']],[vertex_node['y']]]))):
                        r = current_node['r']
                    else:
                        r = current_node['r'] - 1
                    suc['r'] = r
                    suc['h'] = computeH_LKH2(path,suc,uav_data,cfgParams)
                    suc['f'] = t_toSuc + suc['h']
                    L = np.array([L,suc])
    
    return L
    
    
def is_inpath(current = None,suc = None): 
    #This function search if a node has been already visited in the path
    if (ClassDef(current) == 'struct'):
        if (isSamePoint(np.array([[current.x],[current.y]]),suc)):
            is_rel = True
        else:
            is_rel = is_inpath(current.parent,suc)
    else:
        #The last, it will be current.parent == -1, it is not a struct, is a
#double
        is_rel = False
    
    return is_rel
    
    
def isSamePoint(A = None,B = None): 
    bool = A(1,1) == B(1,1) and A(2,1) == B(2,1)
    return bool
    
    
def computeH(path = None,suc = None,uav_data = None): 
    __,c = path.shape
    rnodes = []
    h = 0
    for i in np.arange(2,c+1).reshape(-1):
        if (not is_inpath(suc,path[:,i]) ):
            rnodes = np.array([rnodes,path[:,i]])
    
    if (not len(rnodes)==0 ):
        __,c = rnodes.shape
        for i in np.arange(2,c+1).reshape(-1):
            h = h + EUC_2D_Time(EUC_2D_Distance(path[:,1],path[:,i]),uav_data)
        h = (h / uav_data.Tt) * (uav_data.To + uav_data.Tl + 250)
        h = np.round(h,0)
    
    return h
    
    
    
def computeH_LKH2(path = None,suc = None,uav_data = None,cfgParams = None): 
    #1. Estimate the number of charging stops So = ceil(Sum(EveryRemNodetoHome)/uav_data.Tt);
    __,n = path.shape
    h = 0
    rnodes = np.array([[suc['x']],[suc['y']]])
    costToHome = 0
    for i in np.arange(2,n+1).reshape(-1):
        if (not is_inpath(suc,path[:,i]) ):
            rnodes = np.array([rnodes,path[:,i]])
            costToHome = costToHome + EUC_2D_Time(EUC_2D_Distance(path[:,1],path[:,i]),uav_data)
    
    So = np.int64(np.ceil(costToHome / uav_data.Tt))
    
    if (So > 0):
        #2. Order nodes with LKH solver (Greedy TSP)
        __,n = rnodes.shape
        cost_matrix = []
        for i in np.arange(1,n+1).reshape(-1):
            for j in np.arange(1,n+1).reshape(-1):
                cost_matrix[i,j] = EUC_2D_Time(EUC_2D_Distance(rnodes[:,i],rnodes[:,j]),uav_data)
        if (n > 2):
            LKH_TSP = 'D:\TERRA\EstimatingHeuristic'
            
            TSPsolution,__ = LKH_TSP(cost_matrix,{'CostMatrixMulFactor' : 1,'user_comment' : ''},'tsp_solution',cfgParams.LKHdir,cfgParams.LKHdir)
        else:
            TSPsolution = np.array([1,2,1])
        ordered_nodes = rnodes[:,TSPsolution(1,np.arange(1,n+1))]
        #3. Cluster nodes in 'So' clusters -> idx = kmeans(rnodes,So),, without considering 'suc'
        idx = kmeans(np.transpose(ordered_nodes[:,np.arange(2,n+1)]),So)
        #4. Compute Tf of each cluster from Current_Node to Home
        cluster_matrix = np.zeros((2,So))
        cluster_matrix[2,:] = np.multiply(ordered_nodes(1,1),np.ones((So,1)))
        cluster_matrix[3,:] = np.multiply(ordered_nodes(2,1),np.ones((So,1)))
        for i in np.arange(2,n+1).reshape(-1):
            cluster_matrix[1,idx[i - 1]] = cluster_matrix(1,idx(i - 1)) + EUC_2D_Time(EUC_2D_Distance(cluster_matrix(np.arange(2,3+1),idx(i - 1)),ordered_nodes[:,i]),uav_data)
            cluster_matrix[np.arange[2,3+1],idx[i - 1]] = ordered_nodes[:,i]
        #Sum the cost to return to home
        Tch = mean(costToHome) * 2
        for j in np.arange(1,So+1).reshape(-1):
            cluster_matrix[1,j] = cluster_matrix(1,j) + EUC_2D_Time(EUC_2D_Distance(cluster_matrix(np.arange(2,3+1),j),path[:,1]),uav_data)
            Se = cluster_matrix(1,j) / uav_data.Tt
            h[j] = (Se * Tch) + (2 * cluster_matrix(1,j))
        #6. Final H
        h = sum(h)
    
    return h
    
    
def computeH_LKH3(path = None,suc = None,uav_data = None): 
    #1. Estimate the number of charging stops So = ceil(Sum(EveryRemNodetoHome)/uav_data.Tt);
    __,n = path.shape
    h = 0
    rnodes = np.array([[suc['x']],[suc['y']]])
    costToHome = 0
    for i in np.arange(2,n+1).reshape(-1):
        if (not is_inpath(suc,path[:,i]) ):
            rnodes = np.array([rnodes,path[:,i]])
            costToHome = costToHome + EUC_2D_Time(EUC_2D_Distance(path[:,1],path[:,i]),uav_data)
    
    So = np.int64(int(np.floor(costToHome / uav_data['Tt'])))
    
    if (So > 0):
        #2. Cluster nodes in 'So' clusters -> idx = kmeans(rnodes,So),, without considering 'suc'
        __,n = rnodes.shape
        idx = kmeans(np.transpose(rnodes[:,np.arange(2,n+1)]),So)
        r,__ = idx.shape
        #3. Compute cost matrix of each cluster
        Tf = []
        Tf[1,:] = np.zeros((1,So))
        for k in np.arange(1,So+1).reshape(-1):
            kcluster = np.array([[suc['x']],[suc['y']]])
            for h in np.arange(2,r + 1+1).reshape(-1):
                if (idx(h - 1) == k):
                    kcluster = np.array([kcluster,rnodes[:,h]])
            __,n = kcluster.shape
            cost_matrix = []
            for i in np.arange(1,n+1).reshape(-1):
                for j in np.arange(1,n+1).reshape(-1):
                    cost_matrix[i,j] = EUC_2D_Time(EUC_2D_Distance(kcluster[:,i],kcluster[:,j]),uav_data)
            #4. Compute TSP of each cluster
            if (n > 2):
                LKHdir = 'D:\TERRA\EstimatingHeuristic'
                TSPsolution,TSPcost = LKHdir(cost_matrix,{'CostMatrixMulFactor' : 1,'user_comment' : ''},'tsp_solution',LKHdir,LKHdir)
            else:
                TSPsolution = np.array([1,2,1])
                TSPcost = sum(cost_matrix[1,:])
            #5. Compute Tf = TSPcost
            Tf[So] = Tf(So) + TSPcost - EUC_2D_Time(EUC_2D_Distance(kcluster[:,TSPsolution(n)],kcluster[:,1]),uav_data)
            Tf[So] = Tf(So) + EUC_2D_Time(EUC_2D_Distance(kcluster[:,TSPsolution(n)],path[:,1]),uav_data)
        #6. Sum the cost to return to home
        Tch = mean(costToHome) * 2
        for j in np.arange(1,So+1).reshape(-1):
            Se = Tf(j) / uav_data.Tt
            h[j] = (Se * Tch) + (2 * Tf(j))
        #7. Final H
        h = sum(h)
    
    return h
    
    
def EUC_2D_Distance(last = None,next = None): 
    d = np.sqrt(((last(1,1) - next(1,1)) ** 2) + ((last(2,1) - next(2,1)) ** 2))
    d = np.round(d,4)
    return d
    
    
def EUC_2D_Time(d = None,uav_data = None): 
    t = np.round(d / uav_data.Vuav,0)
    return t
    
    return rte,dist,time,stops