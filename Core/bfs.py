from ast import ClassDef
import numpy as np
import struct

from ismember import ismember
    



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




def bfs(home = None,path = None,current_node = None,uav_data = None): 
    #h = 0;
    OPEN = []
    
    CLOSE = []
    
    
    current_node = {'parent' : current_node['parent'],'x' : current_node['x'],'y' : current_node['y'],'t' : 0,'g' : current_node['g'],'r' : current_node['r']}
    OPEN = np.array([current_node,OPEN])
    while (not len(OPEN)==0 ):

        
        current_node = OPEN(1)
        OPEN = remove(OPEN,current_node)
        if (isSamePoint(np.array([[current_node['x']],[current_node['y']]]),home) and current_node['r'] == 0):
            
            break
        SUCS = expand_graph(current_node,path,home,uav_data)
        __,n_sucs = SUCS.shape
        for i in np.arange(1,n_sucs+1).reshape(-1):
            in_closed = is_visited(CLOSE,SUCS(i))
            if (0 == in_closed):
                in_open = is_visited(OPEN,SUCS(i))
                if (0 == in_open):
                    OPEN = np.array([SUCS(i),OPEN])
        CLOSE = np.array([CLOSE,current_node])

    
    return current_node
    
    
def expand_graph(current_node = None,path = None,home = None,uav_data = None): 
    __,c = path.shape
    SUCS = []
    for i in np.arange(1,c+1).reshape(-1):
        suc = np.array([[path(1,i)],[path(2,i)]])
        if (not isSamePoint(np.array([[current_node['x']],[current_node['y']]]),suc) ):
            if (isSamePoint(home,suc)):
                is_rel = False
            else:
                is_rel = is_inpath(current_node,suc)
            if (not is_rel ):
                d_toSuc = EUC_2D_Distance(np.array([[current_node['x']],[current_node['y']]]),suc)
                t_toSuc = EUC_2D_Time(d_toSuc,uav_data)
                if (isSamePoint(np.array([[current_node['x']],[current_node['y']]]),home)):
                    g = uav_data['To'] + t_toSuc
                    t_toSuc = current_node['t'] + uav_data['To'] + t_toSuc
                else:
                    g = current_node['g'] + t_toSuc + uav_data['Tg']
                    if (isSamePoint(suc,home)):
                        tc = uav_data['Tt'] - g
                        t_toSuc = current_node['t'] + t_toSuc + uav_data['Tl'] + tc
                    else:
                        t_toSuc = current_node['t'] + t_toSuc
                d_tohome = EUC_2D_Distance(home,suc)
                t_tohome = EUC_2D_Time(d_tohome,uav_data)
                if (uav_data['Tt'] >= int(np.floor(g + t_tohome + uav_data['Tl']))):
                    suc = {'parent' : current_node,'x' : suc(1,1),'y' : suc(2,1),'t' : t_toSuc,'g' : g,'r' : 0}
                    if (isSamePoint(np.array([[suc['x']],[suc['y']]]),home)):
                        suc['r'] = current_node['r']
                    else:
                        suc.r = current_node['r'] - 1
                    SUCS = np.array([SUCS,suc])
    
    return SUCS
    
    
def is_visited(list = None,node = None): 
    nodeIdx = 0
    if (not len(list)==0 ):
        list = myStruct2table(list)
        list = np.array([list[:,np.arange(2,4+1)],list[:,6]])
        node = myStruct2table(node)
        node = np.array([node[:,np.arange(2,4+1)],node[:,6]])
        r,__ = list.shape
        for i in np.arange(1,r+1).reshape(-1):
            if (list[i,:] == node[1,:]):
                nodeIdx = i
                break
    
    return nodeIdx
    
    
def isSamePoint(A = None,B = None): 
    bool = A(1,1) == B(1,1) and A(2,1) == B(2,1)
    return bool
    
    
def is_inpath(current = None,suc = None): 
    #This function search if a node has been already visited in the path
    if (ClassDef(current) == 'struct'):
        if (isSamePoint(np.array([[current.x],[current.y]]),suc)):    
            is_rel = True
        else:
            is_rel = is_inpath(current.parent,suc)
    else:
       
        is_rel = False
    
    return is_rel
    
    
def remove(OPEN = None,suc = None): 
    list = OPEN
    if (not len(list)==0 ):
        list = myStruct2table(list) 
        list = np.array([list[:,np.arange(2,4+1)],list[:,6]])
        suc = myStruct2table(suc)
        suc = np.array([suc[:,np.arange(2,4+1)],suc[:,6]])
        __,Locb = ismember(list,suc,'rows')
        idx = str.find(Locb,1)
        OPEN(idx).f = np.inf
        OPEN = deleteNode(OPEN)
    
    return OPEN
    
    
def deleteNode(OPEN = None): 
    L = []
    __,c = OPEN.shape
    for i in np.arange(1,c+1).reshape(-1):
        if (OPEN(i).f != np.inf):
            L = np.array([L,OPEN(i)])
    
    OPEN = L
    return OPEN
    
    
def EUC_2D_Distance(last = None,next = None): 
    d = np.sqrt(((last(1,1) - next(1,1)) ** 2) + ((last(2,1) - next(2,1)) ** 2))
    d = np.round(d,4)
    return d
    
    
def EUC_2D_Time(d = None,uav_data = None): 
    t = np.round(d / uav_data.Vuav,0)
    return t
    
    return current_node