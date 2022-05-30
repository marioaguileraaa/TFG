# This function solves the TSP for the UGV in the TERRA algorithm.

# INPUTS
# V3: list of vertices
# ugv_tsp: UGV's TSP Genetic Algoritm Parameters

# OUTPUT
# UGV_path: LoL

from gettext import find
from math import dist
import numpy as np
import numpy as geek
# Importing the statistics module
import statistics
# Importing the statistics module
from statistics import mean

from numpy.random.mtrand import randn
# import pytorch library
import torch
# importing numpy as geek 
import numpy as geek
import builtins
import itertools
    
def tsp_ga_ugv(V3 = None,ugv_tsp = None): 
    # Load Instance
    totalDistTest = list()
    """
    print('V3')
    print(V3)
    print('V3[0]')
    print(V3[0])
    print('V3[1]')
    print(V3[1])
    print('V3[0][0]')
    print(V3[1][0])
    """
    V3_aux = [V3[0][0], V3[1][0]]
    """
    print('V3_aux')
    print(V3_aux)
    print('V3_aux[0]')
    print(V3_aux[0])
    print('V3_aux[1]')
    print(V3_aux[1])
    """
    xy_aux = np.transpose(V3_aux)
    xy = xy_aux
    last_depot = 1
    popSize = ugv_tsp['popSize']
    tournaments = ugv_tsp['tournaments']
    mutOper = ugv_tsp['mutOper']
    mutRate = ugv_tsp['mutRate']
    crossOper = ugv_tsp['crossOper']
    eliteP = ugv_tsp['eliteP']
    # Set Fixed Seval and compute the remaining parameters
    seval = 30000
    numIter = seval / popSize
    elite = popSize * eliteP / 100
    # Initialize default configuration of the genetic algorithm
    dmat = []
    minDist = 0
    elitesMut = mutRate * popSize
    if len(dmat)==0:
        #nPoints = xy.shape[1-1]
        nPoints = len(xy)
        #a = np.meshgrid(np.arange(1,nPoints+1))  #no hace bien el meshgrid
        a = []
        
        #meshgrid
        lista_aux = list()
        for i in range(1, nPoints+1):
            lista_aux.append(i)
        for i in range(0, nPoints):
            a.append(lista_aux)         
        a = np.array(a)
        indice = 0
        lista_xy_a = list() #es lo mismo que xy[a,:] en matlab
        for i in a:
            for i2 in a:
                lista_xy_a.append(xy[i2[indice] -1])
            indice = indice +1
        lista_xy_a = np.array(lista_xy_a)    
        a_transpose = np.transpose(a)
        indice = 0
        lista_xy_a_transpose = list() #es lo mismo que xy[a_transpose,:] en matlab
        for i in a_transpose:
            for i2 in a_transpose:
                lista_xy_a_transpose.append(xy[i2[indice] -1])
            indice = indice +1
        lista_xy_a_transpose = np.array(lista_xy_a_transpose)    
        aux_dmat = np.sum((lista_xy_a - lista_xy_a_transpose) ** 2, 1)
        aux_dmat_np = []
        for i in aux_dmat:
            aux_dmat_np.append([i])
        aux_dmat_np = np.array(aux_dmat_np) 
        dmat_sqrt =   np.sqrt( aux_dmat_np)
        dmat_aux = dmat_sqrt.reshape(nPoints,nPoints)
        dmat = dmat_aux
    N,__ = xy.shape
    nr,nc = dmat.shape
    if N != nr or N != nc:
        raise Exception('Invalid XY or DMAT inputs!')
    
    n = N
    # Sanity Checks
    popSize = 4 * np.ceil(popSize / 4)
    """
    print('valor inicial numIter')
    print(numIter)
    print('numIter(1)')
    print(numIter(1))
    print('np.real(numIter(1)')
    print(np.real(numIter(1))) 
    print('np.round(np.real(numIter(1)))')
    print(np.round(np.real(numIter(1))))
    """
    
    numIter = max(1, np.round(numIter))
    a = (int(popSize),int(n-1))
    pop = np.zeros(a)
    n_aux = []
    for i in range (1, n):
        n_aux.append(i)
    
    for k in np.arange(0,int(popSize)).reshape(-1):
        pop[k] = np.random.permutation(n_aux) 
    # Run the GA
    globalMin = np.inf
    totalDist = np.zeros((1,int(popSize)))
    distHistory = np.zeros((3,int(numIter)))
    tmpPop = np.zeros((1,int(n-1)))
    for iter in np.arange(0,numIter).reshape(-1):
        newPop = []
        popSize = len(pop)
        for p in np.arange(0,len(pop)).reshape(-1):
            if (last_depot == 1):
                #
                p = int(p)
                #n = n-1
                #
                """
                print('pop')
                print(pop)
                print('p '+str(p))
                print('n -1'+str(n-1))
                print('n'+str(n))
                print(pop[p][n-1])
                print(pop[p][1])
                """
                """
                print('for ebtre 0 y '+str(popSize))
                print('p vale '+str(p))
                print('n vale '+str(n))
                print('len pop  vale '+str(len(pop)))
                """
                if p >= len(pop): 
                    resto = p - len(pop) +2
                    print('rest es '+str(resto))
                    d = np.round(dmat[int(pop[p-resto][n -2] -1)][int(pop[p-resto][1] -1)], 2)
                else:
                   d = np.round(dmat[int(pop[p][n -2] -1)][int(pop[p][1] -1)], 2)
            else:
                d = 0
            for k in np.arange(1,n-1).reshape(-1):
                if p >= len(pop): 
                    resto = p - len(pop) +2
                    print('rest es '+str(resto))
                    d = d + dmat[int(pop[p-resto][k-1] -1)][int(pop[p-resto][k] -1)]
                else:
                   d = d + dmat[int(pop[p][k-1] -1)][int(pop[p][k] -1)]
                    
            totalDist[0][p-1] = d
        for i in totalDist[0]:
            totalDistTest.append(i)
        
        minDist = np.amin(totalDist[0])
        index = np.where(minDist == np.amin(totalDist[0]))
        iter = int(iter)
        distHistory[0][iter] = minDist
        if minDist < globalMin:
            globalMin = minDist
            optRoute = pop[index]
        distHistory[1][iter] = mean(totalDist[0])
        maxDist = max(totalDist[0])
        distHistory[2][iter] = maxDist
        #Only for demonstrating to a reviewer an issue
        if (iter > 40):
            elitesMut = 0
        # Mutation Operator for the Genetic Algorithm
        #for p in np.arange(1,elitesMut+1).reshape(-1):
        #print('elites mut '+str(elitesMut))
        newPop = list()
        for p in np.arange(0,int(elitesMut)).reshape(-1):
            randIdx = np.ceil(1 + (popSize - 1) * np.random.rand(1,tournaments))
           
            indice = 0
            lista_pop_randIdx = list() #es lo mismo que pop[randIdx,:] en matlab
            
            for i2 in randIdx:
                for i in i2:
                    lista_pop_randIdx.append(pop[int(i -1)])
            rtes = np.array(lista_pop_randIdx)   
            dists = list()
            indice = 0
            for i in randIdx[0]:
             
             dists.append(totalDist[0][int(i-1)])
             indice = indice +1
            dists = np.array(dists) 
            aux_1 = np.amin(dists[0])
            idx = np.where(aux_1 == np.amin(dists[0]))[0]
            best = rtes[int(idx)] 
            routeInsertionPoints = np.sort(np.ceil((n-1) * np.random.rand(1,2))) #igual 0,1
            I = routeInsertionPoints[0][0]
            J = routeInsertionPoints[0][1]
            tmpPop[0] = best
            if 1 == mutOper:   
                print('np.arange(J,I+- 1,- 1)')
                print(np.arange(J,I+- 1,- 1))
                print('np.arange[I,J+1]')
                print(np.arange[I,J+1])
                tmpPop[1,np.arange[I,J+1]] = tmpPop(1,np.arange(J,I+- 1,- 1))
            else:
                if 2 == mutOper: #REVISADO..
                    aux_pop =list()
                    for i in [J, I]:
                        aux_pop.append(tmpPop[0][int(i-1)]) #quito 1 porque 1, 2 esta fuera de 0,1 
                    aux_pop =  np.array(aux_pop)
                    index = 0
                    for i in [I,J]:
                        tmpPop[0][int(i -1)] = aux_pop[index]
                        index = index +1
                else:
                    if 3 == mutOper: 
                        tmpPop[1,np.arange[I,J+1]] = tmpPop(1,np.array([np.arange(I + 1,J+1),I]))
            newPop.append(tmpPop[0])
        newPop = np.array(newPop)   
        if (elitesMut > 0):
            #Mecanismo para mantener el tamaño de la población
            r = len(newPop)
            restPop = popSize - r
        else:
            restPop = popSize
        #Elitism Selection Mechanism
        if (elite > 0):
            restPop = restPop - elite
            tmpTotalDist = totalDist
            p = 0
            while (p < elite):
                aux_1 = np.amin(totalDist[0])
                index = np.where(aux_1 == np.amin(dists[0]))[0]
                tmpTotalDist[index] = tmpTotalDist[index] + np.inf
                try:
                    newPop = np.concatenate((newPop, pop[index]))
                except:
                    newPop =  pop[index]
                    print('except.')
                    print('newpop')
                    print(newPop)
                p = p + 1

        tmpPop = np.zeros((1,n))
        while (restPop > 0):
            randomOrder = np.random.permutation(int(popSize))
            firstParent = np.zeros((1,n))
            secondParent = np.zeros((1,n))
            randIdx = np.ceil(tournaments + (popSize - tournaments) * np.random.rand(1,1))
            indice = 0
            lista_pop_randomOrder = list() #es lo mismo que pop[randomOrder,:] en matlab
            for i2 in randomOrder:
                    lista_pop_randomOrder.append(pop[int(i2 -1)])
            rtes = np.array(lista_pop_randomOrder)   
            lista_aux_indices = np.arange(randIdx - tournaments + 1,randIdx+1)
            dists = list()
            indice = 0
            for i in lista_aux_indices:
             dists.append(totalDistTest[int(i-1)])
             indice = indice +1
            dists = np.array(dists)
            dists = np.array([dists])
            aux_1 = np.amin(dists[0])
            idx = np.where(aux_1 == np.amin(dists[0]))[0]
            firstParent = rtes[idx]
            dists[0][idx] = + np.inf
            aux_1 = np.amin(dists[0])
            idx = np.where(aux_1 == np.amin(dists[0]))[0]
            secondParent = rtes[idx]
            if 1 == crossOper:
                tmpPop = OX(firstParent,secondParent)
                restPop = restPop - 1
            else:
                if 2 == crossOper:
                    tmpPop = CX(firstParent,secondParent)
                    restPop = restPop - 2
                    if (restPop < 0):
                        aux = tmpPop[1,:]
                        tmpPop = []
                        tmpPop = aux
                else:
                    if 3 == crossOper:
                        tmpPop = OBX(firstParent,secondParent)
                        restPop = restPop - 1           
            newPop = np.concatenate((newPop, tmpPop))

        pop = newPop
    
    print('optRoute')
    print(optRoute)
    idx = ''
    index_au = 0
    for i in optRoute[0]:
        if i == 1: 
            idx = index_au
        index_au = index_au +1    

    
    print('idx')  
    print(idx)
    len_ = len(optRoute[0]) #posiblemente [0]
    print('len_') 
    print(len_)
    
    cycles = len_ - idx 
    print('optRoute')
    print(optRoute) 
    print('cycles')
    print(cycles)    
    rte = np.roll(optRoute,cycles)  #Circshift = np.roll   
    print('rte  np roll')
    print(rte) #[2. 1.], debe ser 1 2 
    if last_depot == 1:
        
        print('last_depot')
        print(last_depot)
        rte = rte[0]
        print('rte 1')
        print(rte)
        list_rte = list()
        for i in rte:
              list_rte.append(i)
        list_rte.append(last_depot)    
        rte = np.array(list_rte)  
        print('rte 2')
        print(rte) #[2. 1. 1.]
        
        
    print('rte')
    print(rte) #[2. 1. 1.]
    print('V3')
    print(V3)
    #UGV_path = np.array([[V3[0][rte]],[V3[1][rte]]])  #aqui sera un [][] y ver porque rte es un array...
    UGV_path_x = list()
    UGV_path_y = list()
    for i in rte:
        UGV_path_x.append(V3[0][0][int(i-1)])
        UGV_path_y.append(V3[1][0][int(i-1)])
    UGV_path_x  = np.array(UGV_path_x)  
    UGV_path_y  = np.array(UGV_path_y) 
    UGV_path = np.array([UGV_path_x,UGV_path_y])  #aqui sera un [][] y ver porque rte es un array...
    print('UGV_path')
    print(UGV_path)
    UGV_path = np.transpose(UGV_path)
    print('UGV_path')
    print(UGV_path)
    print('resultados')
    print(rte)
    print(minDist)
    print(UGV_path)
    return rte,minDist,UGV_path 
    #tiene coerencia con lo de matlab solo que  los valores al ser aleatorios
    #no coinciden exactamente al depender del rte y minDist. 
    
    
def OX(p1 = None,p2 = None): 
    c1 = len(p1[0])
    c2 = len(p2[0])
    child = np.array([])
    list_child = list()
    list_child.append(-1)
    for i in range (1, c1):
        list_child.append(-1)
    list_child = np.array(list_child)   
    child = [list_child] 
    
    randIdx1 = builtins.sorted(np.ceil(1 + (c1 - 1) * np.random.rand(1,2)))
    child[0][int(np.arange(randIdx1[0][0],randIdx1[0][1]+1)[0]-1)] = p1[0][int(np.arange(randIdx1[0][0],randIdx1[0][1]+1)[0]-1)]
    for p in np.arange(0,c2 -1).reshape(-1):
        index = 0
        k = ''
        for i in child[0]:
                if int(i) == int(p2[0][p]):
                    k = index
                index = index +1
        if (len(k)==0):
            pos = 0
            t = 0
            pos_aux = -1
            #while (pos == 0):
            while (pos_aux == -1):
                """
                print('valor de t'+ str(t))
                print('child[0][t]')
                print(child[0][t])
                """
                if (child[0][t] == -1):
                    #print('dentro')
                    pos = t
                    pos_aux = t
                    #print('pos es '+str(pos))
                t = t + 1
                
            child[0][pos] = p2[0][p]
            
    return child
    
    
def CX(parent1 = None,parent2 = None): 
    totalCycles = []
    childs = []
    __,c = parent1.shape
    completed = False
    #Compute N cycles, till parent1 = []
    while (not completed ):

        cycleN,parent1,parent2 = cycling(parent1,parent2)
        totalCycles = np.array([[totalCycles],[cycleN]])
        count = 0
        for h in np.arange(1,c+1).reshape(-1):
            if (parent1(1,h) == - 1):
                count = count + 1
        if count == c:
            completed = True

    
    #Filling the new chromosomes
    r,n = totalCycles.shape
    numCycles = r / 2
    c = 0
    for i in np.arange(1,numCycles+1).reshape(-1):
        p = np.mod(i,2)
        if p == 1:
            for j in np.arange(1,n+1).reshape(-1):
                if (totalCycles(i + c,j) != - 1):
                    childs[1,j] = totalCycles(i + c,j)
                if (totalCycles(i + c + 1,j) != - 1):
                    childs[2,j] = totalCycles(i + c + 1,j)
        else:
            for j in np.arange(1,n+1).reshape(-1):
                if (totalCycles(i + c,j) != - 1):
                    childs[2,j] = totalCycles(i + c,j)
                if (totalCycles(i + c + 1,j) != - 1):
                    childs[1,j] = totalCycles(i + c + 1,j)
        c = c + 1
    
    return childs
    
    
def OBX(parent1 = None,parent2 = None): 
    __,c = parent1.shape
    child = []
    child[1,np.arange[1,c+1]] = - 1
    #Step 1: Random indexs
    set = np.ceil(1 + (c - 1) * np.random.rand(1,1))
    selectedPositions = randn(set)
    selectedinP1 = parent1(selectedPositions)
    #Step 2: Copy parent2 to child
    for i in np.arange(1,c+1).reshape(-1):
        if (len(str.find(selectedinP1 == parent2(1,i),1))==0):
            child[1,i] = parent2(1,i)
    
    #Step 3: Copy parent1 to child
    for i in np.arange(1,c+1).reshape(-1):
        if (not len(str.find(selectedinP1 == parent1(1,i),1))==0 ):
            for j in np.arange(1,c+1).reshape(-1):
                if (child(1,j) == - 1):
                    child[1,j] = parent1(1,i)
                    break
    
    return child
    
    
def cycling(parent1 = None,parent2 = None): 
    __,c = parent1.shape
    cycle = []
    cycle[np.arange[1,2+1],np.arange[1,c+1]] = - 1
    #Find first element of the new parent
    r = 1
    while (parent1(1,r) == - 1):

        r = r + 1

    
    cycle = find_cycle(cycle,parent1(1,r),parent1(1,r),parent1,parent2)
    #Update new parents
    newParent1 = []
    for p in np.arange(1,c+1).reshape(-1):
        idx = str.find(cycle[1,:] == parent1(1,p))
        if len(idx)==0:
            newParent1 = np.array([newParent1,parent1(1,p)])
        else:
            newParent1 = np.array([newParent1,- 1])
    
    newParent2 = []
    for p in np.arange(1,c+1).reshape(-1):
        idx = str.find(cycle[2,:] == parent2(1,p))
        if len(idx)==0:
            newParent2 = np.array([newParent2,parent2(1,p)])
        else:
            newParent2 = np.array([newParent2,- 1])
    
    return cycle,newParent1,newParent2
    
    
def find_cycle(cycle = None,currValue = None,initValue = None,parent1 = None,parent2 = None): 
    idx = str.find(parent1 == currValue)
    cycle[1,idx] = currValue
    currValue = parent2(1,idx)
    cycle[2,idx] = currValue
    t = len(cycle)
    if (t == 1):
        initValue = cycle(1,idx)
    else:
        if (t > 1):
            if (initValue != parent2(1,idx)):
                cycle = find_cycle(cycle,currValue,initValue,parent1,parent2)
    
    return cycle
    
    return rte,minDist,UGV_path