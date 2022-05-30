
import numpy as np
from ismember import ismember
import struct
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

    
    
def search_uav_path(subpath = None,uav_data = None): 
    Radius = uav_data['R']
    path = subpath
    home = np.array([[path[0][0]],[path[1][0]]])
    stops = 0
    #N = n� total of nodes
    N = len(path[0])
    h = N - 1
    #Start Node: g = 0 : k = 0 : h = N-1 : f = g + h
    
    #start_node = struct('parent',- 1,'x',path(1,1),'y',path(2,1),'g',0,'k',0,'h',h,'f',h)
    start_node = {'parent' : - 1,'x' : path[0][0],'y' : path[1][0],'g' : 0,'k' : 0,'h' : h,'f' : h}
    start_node_aux = {'parent' : - 1,'x' : start_node['x'],'y' : start_node['y'],'g' : start_node['g'],'k' : start_node['k'],'h' : start_node['h'],'f' : start_node['f']}
    start_node = {'parent' : - 1,'x' : start_node_aux['x'],'y' : start_node_aux['y'],'g' : start_node_aux['g'],'k' : start_node_aux['k'],'h' : start_node_aux['h'],'f' : start_node_aux['f']}

    sol_found = False
    dist = 0
    rte = []
    # The ordered list of currently discovered nodes that are not evaluated yet.
# Initially, only the start node is known.
    
    
    #NECESITO PODER ANADIR DICTS EN DICTS, PARA ELLO HAGO UN LISTADO DE DICTS. 
    OPEN = list()
    OPEN.append(start_node)
    #OPEN = start_node
    CLOSED = list()
    while (not len(OPEN)==0 ):
        print('OPEN')
        print(OPEN)
        current_node,OPEN = find_lowest(OPEN)
        print('current_node')
        print(current_node) 
        print('OPEN')
        print(OPEN)
        current_node  = {'parent' : current_node['parent'],'x' : current_node['x'],'y' : current_node['y'],'g' : current_node['g'],'k' : current_node['k'],'h' : current_node['h'],'f' : current_node['f']}
        print('start_node del while')
        print(start_node)  
        start_node = {'parent' : - 1,'x' : start_node['x'],'y' : start_node['y'],'g' : start_node['g'],'k' : start_node['k'],'h' : start_node['h'],'f' : start_node['f']}
          
        
        
        
        #HASTA AQUI BIEN, SEGUIR...
        #CUIDADO AL IGUAL UNA VARIABLE A OTRA, PORQUE SI CAMBIA PUES CAMBIA LA OTRA SIN QUERER.
        #HAY QUE IGUALAR COGIENDO LOS DATOS COMO TAL COMO EN FIND_LOWEST()
        #EJ:
        ##node = OPEN(j) SERIA EN ESTE CASO LO SIGUIENTE.
        #node = {'parent' : OPEN[j]['parent'],'x' : OPEN[j]['x'],'y' : OPEN[j]['y'],'g' : OPEN[j]['g'],'k' : OPEN[j]['k'],'h' : OPEN[j]['h'],'f' : OPEN[j]['f']}
                





        #Delete current_node from OPEN
        
        OPEN[0]['f']  = np.inf 
        print('open antes de deleteNode')
        print(OPEN)
        OPEN = deleteNode(OPEN)
        print('Open despues de deleteNode')
        print(OPEN)
        ##Goal Node is HOME with h=0
        if ((current_node['x'] == home[0][0]) and (current_node['y'] == home[1][0]) and (current_node['h'] == 0)):
            sol_found = True
            break
        print('variables de funcion expand_grapha antes de entrar')
        print('current_node')
        print(current_node) 
        print('path')
        print(path) 
        print('Radius')
        print(Radius)
        print('start_node')
        
        start_node = {'parent' : - 1,'x' : start_node_aux['x'],'y' : start_node_aux['y'],'g' : start_node_aux['g'],'k' : start_node_aux['k'],'h' : start_node_aux['h'],'f' : start_node_aux['f']}
    
        print(start_node) 
        print('start_node_aux')
        print(start_node_aux) 
        
        
        SUCS = expand_graph(current_node,path,Radius,start_node)
        print('variable return de expand grapth es ')
        print('sucs')
        print(SUCS) 
        
        #Check if those successors has been visited yet
        #print('\n\nSUCS') #tiene pinta de estar mal.....mirar funcion que lo crea.
        #debe ser como OPEN de formato.
        n_sucs = len(SUCS)
        print('n_sucs')
        print(n_sucs)
        print('\n\n\n\n')
        for i in np.arange(0,n_sucs).reshape(-1):
            in_closed = is_visited(CLOSED,SUCS[i])
            if (not in_closed ):
                in_open = is_visited(OPEN,SUCS[i])
                if (not in_open ):
                    SUCS[i]['g'] = + np.inf
                    SUCS[i]['parent'] = '' 
                OPEN = UpdateVertex(OPEN,current_node,SUCS[i])
        #Put current_node in list of nodes currently visited CLOSED
        CLOSED.append(current_node)
    
    
    
    if (sol_found): 
        rte,dist = reconstruct_path(current_node,rte,dist,path)  
        c = len(rte)
        for i in np.arange(1,c - 1).reshape(-1):
            if (rte[i] == 0):
                stops = stops + 1
    else:
        print('UAV Subpath solution NOT found!')
    
    return rte,dist,stops
    
    
def UpdateVertex(OPEN = None,current_node = None,suc = None): 
    d = np.sqrt(((suc['x'] - current_node['x']) ** 2) + ((suc['y'] - current_node['y']) ** 2))
    if (current_node['g'] + d < suc['g']):
        suc['g'] = current_node['g'] + d
        suc['parent'] = -1
        in_open = is_visited(OPEN,suc)
        if (in_open):
            OPEN = remove(OPEN,suc)
        suc['f'] = suc['g'] + suc['h']
        
        
        OPEN.append(suc)
        
    
    return OPEN
    
    
def remove(OPEN = None,suc = None): 
    list = OPEN
    if (not len(list)==0 ):
        list = myStruct2table(list)
        list = np.array([list[:,np.arange(2,3+1)],list[:,6]])
        suc = myStruct2table(suc)
        suc = np.array([suc[:,np.arange(2,3+1)],suc[:,6]])
        __,Locb = ismember(list,suc,'rows')
        idx = str.find(Locb,1)
        OPEN(idx).f = np.inf
        OPEN = deleteNode(OPEN)
    
    return OPEN
    
    
def is_visited(list = None,node = None): 
    in_list = 0
    
    #el primero llega vacio:
    list_tmp = []
    for i in range (0,len(list)):
        if i != 0:
         list_tmp.append(list[i])
    list = list_tmp    
    #fin el primero llega vacio:
    

    if (not len(list)==0 ):
        print('list antes del todo')
        #list = myStruct2table(list)
        #paso el dict a listado para usarlo como table que lo usan en matlab...
        #en matlab es solo un dict: 
        #list = list[0]
        #list = '{\'parent\': -1, ' + list[0].split('},')[1]
        """
        list_aux2 = []
        list_aux2.append(list[0]['parent'])
        list_aux2.append(list[0]['x'])
        list_aux2.append(list[0]['y'])
        list_aux2.append(list[0]['g'])
        list_aux2.append(list[0]['k'])
        list_aux2.append(list[0]['h'])
        list_aux2.append(list[0]['f'])
        list = list_aux2
        """
        #me TENGO QUE QUEDAR SOLO CON ALGUNOS VALORES.. FACIL...

        list_aux2 = []
        list_aux2.append(list[0]['x'])
        list_aux2.append(list[0]['y'])
        list_aux2.append(list[0]['h'])
        #print('node')
        node = [node]
        #print(node)
        node_ux2 = []
        node_ux2.append(node[0]['x'])
        node_ux2.append(node[0]['y'])
        node_ux2.append(node[0]['h'])
        #list = list_aux2
        #list = np.array([list[:,np.arange(2,3+1)],list[:,6]])
        """
        print('list desp')
        print(list)
        print('node antes antes')
        print(node)
        node = myStruct2table(node)
        print('node antes')
        print(node)
        node = np.array([node[:,np.arange(2,3+1)],node[:,6]])
        print('node desp')
        print(node)
        in_list = sum(ismember(list,node,'rows')) >= 1
        print('in_list')
        print(in_list)
        """
        #print(node_ux2)
        #print(list_aux2)
        if node_ux2 == list_aux2:
            in_list = 1
        else:
            in_list = 0    
        #devuleve un 1 si node y list son iguales 100%, sino un 0
    return in_list
    
    
def deleteNode(OPEN = None): 
    L = list()
    #print('dentro de funcion: deleteNode')
    
    #__,c = OPEN.shape #como ahsta ahora, esto es 1 siempre..
    c = len(OPEN)
    for i in np.arange(0,c).reshape(-1):
        #if (OPEN(i).f != np.inf): 
        if (OPEN[i]['f'] != np.inf): 
            #L = np.array([L,OPEN(i)]) #L esta vacio .....
            L.append(OPEN[i])
    
    OPEN = L
    #print('acabamos funcion delete ')
    return OPEN
    
    
def reconstruct_path(current_node = None,rte = None,dist = None,path = None): 
    
    __,c = path.shape
    print('path')
    print(path)
    print('c')
    print(c)
    print('rte')
    print(rte)
    
    for i in np.arange(0,c).reshape(-1):
        if (current_node['x'] == path[0][i] and current_node['y'] == path[1][i]):
            #rte = np.array([i,rte])
            print('rte antes')
            print(rte)
            rte.insert(0, i) #giual añadir i +1
            #rte.insert(0, i+1) #giual añadir i +1
            print('rte desp')
            print(rte)
            print('\n')
            aux = str(type(current_node['parent']))
            #aux = str(type(current_node)) 
            print('aux')
            print(aux)
            
            if ('dict' in aux):
            #if (ClassDef(current_node.parent) == 'struct'):
                
                dist = dist + np.sqrt(((current_node['x'] - current_node['parent']['x']) ** 2) + ((current_node['y'] - current_node['parent']['y']) ** 2))
                print('dist desp')
                print(dist)
                rte[100]  #fallo aposta
                rte,dist = reconstruct_path(current_node['parent'],rte,dist,path)
                break
    return rte,dist
    

# COMO UN ARRAY...     
def find_lowest(OPEN = None): 
    #This function order the OPEN list from the node with the lowest F value to
#the node with the highest F value
    print('OPEN find lowest inicial....')
    print(OPEN)
   
    
    co = len(OPEN)
    L = list()
    #L = []
    #lowest = 1
    lowest = 0 #mio aqui pongo 0, mirar si esta bien o debe ser 1...
    #__,cl = L.shape
    #aqui por como es L, tambien es 0
    cl = 0 #mio
    print('lowest')
    print(lowest)
    print('cl')
    print(cl)
    print('co')
    print(co)
    while (cl < co):

        #for j in np.arange(1,co+1).reshape(-1):
        for j in np.arange(0,co).reshape(-1):
            print('for 1')
            #if (OPEN(j).f != np.inf):
            if (OPEN[j]['f'] != np.inf): #como len open es 1, ...quito el j...
                print('if 1, con j valor '+str(j))
                #node = OPEN(j)
                node = {'parent' : OPEN[j]['parent'],'x' : OPEN[j]['x'],'y' : OPEN[j]['y'],'g' : OPEN[j]['g'],'k' : OPEN[j]['k'],'h' : OPEN[j]['h'],'f' : OPEN[j]['f']}
                #node = OPEN[j]
                print('valor de node')
                print(node)
                lowest = j
                break
        print('if  2')   
        print(type(node)) 
        #if (ClassDef(node) == 'struct'):
        aux = str(type(node))
        
        #if (type(node) == '<class \'dict\'>'):
        print('compruebo si es struct')
        print('OPEN(i)')
        print(OPEN)
        if ('dict' in aux): #debe serlo ...
            print('for 2 previo')
            for i in np.arange(0,co).reshape(-1): #igual de c0 -1
                print('for 2')
                print('el valor de i es '+str(i))
                if (OPEN[i]['f'] != np.inf):  #al comienzo debe serlo  
                    print(OPEN[i]['f'])
                    if (OPEN[i]['f'] < node['f']): #
                        print('if 4')
                        node = {'parent' : OPEN[i]['parent'],'x' : OPEN[i]['x'],'y' : OPEN[i]['y'],'g' : OPEN[i]['g'],'k' : OPEN[i]['k'],'h' : OPEN[i]['h'],'f' : OPEN[i]['f']}
                        lowest = i
            
            OPEN[lowest]['f'] = np.inf
            
            L.append(node)
            node = np.inf
            cl = len(L)
    
    node = L[0]
    print('node return ')
    print(node)
    print('--------------------------------------------FIN ----------------------------------------')
    print('--------------------------------------------FIN ----------------------------------------')
    print('--------------------------------------------FIN ----------------------------------------')
    return node,L
    
    
def expand_graph(current_node = None,path = None,Radius = None,start_node = None): 
    __,c = path.shape
    L = list()
    home = np.array([[start_node['x']],[start_node['y']]])
    for i in np.arange(0,c).reshape(-1):
        suc = np.array([[path[0][i]],[path[1][i]]])
        #If current node is not the root of the tree, and the successor it is
#not this same point
        if (int(np.floor(current_node['x'])) != int(np.floor(suc[0][0])) or int(np.floor(current_node['y'])) != int(np.floor(suc[1][0]))):
            #if (current_node.x ~= suc(1,1) || current_node.y ~= suc(2,1))
#Check if node(i) is a relative of the current node
            if (suc[0][0] == start_node['x'] and suc[1][0] == start_node['y']):
                is_rel = False
            else:
                is_rel = is_relative(current_node,suc)
            if (not is_rel ):
                if (current_node['x'] == start_node['x'] and current_node['y'] == start_node['y']):
                    k = np.sqrt(((path[0][i] - current_node['x']) ** 2) + ((path[1][i] - current_node['y']) ** 2))
                else:
                    k = current_node['k'] + np.sqrt(((path[0][i] - current_node['x']) ** 2) + ((path[1][i] - current_node['y']) ** 2))
                g = current_node['g'] + np.sqrt(((path[0][i] - current_node['x']) ** 2) + ((path[1][i] - current_node['y']) ** 2))
                d_tohome = np.sqrt(((path[0][i] - start_node['x']) ** 2) + ((path[1][i] - start_node['y']) ** 2))
                #The UAV has enough energy to go this successor node and return to home
                if (Radius * 2 >= int(np.floor(k + d_tohome))):
                    print('suc')
                    print(suc)
                    print('home')
                    print(home)
                    comparison = suc == home
                    equal_arrays = comparison.all()
                    #if (suc == home):
                    if (equal_arrays):
                        h = current_node['h']
                    else:
                        h = current_node['h'] - 1
                    #No relative, so, we add the successor to the OPEN List
                    
                    suc = {'parent' : -1,'x' : path[0][i],'y' : path[1][i],'g' : g,'k' : k,'h' : h,'f' : g + h}
                    print('L antes')
                    print(L)
                    print('suc antes')
                    print(suc)
                    L.append(suc)
                    print('L despues')
                    print(L)
    return L
    
    
def is_relative(current = None,suc = None): 
    #This function search if a node has been already visited in the path
    if (ClassDef(current) == 'struct'):
        if (current.x == suc(1,1) and current.y == suc(2,1)):
            is_rel = True
        else:
            is_rel = is_relative(current.parent,suc)
    else:
        #The last, it will be current.parent == -1
        is_rel = False
    
    return is_rel
    
    return rte,dist,stops