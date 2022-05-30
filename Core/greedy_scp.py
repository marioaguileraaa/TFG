# MODIFIED VERSION [SolC,SolL] = GREEDYSCP(vx_sol, vy_sol, wp_c): where
# vx_sol is the 'x' coordinate of the vertexes of the solution and vy is the
# 'y' coordinate of the vertexes of the solution, and wp_c the list of all
# the covered waypoints.
# The OUTPUT is the same of the previous version (see below).

# GREEDYSCP Greedy SCP algorithm:: function [solution_setsCell, solution_setsLabelsV] = greedyscp(setsCell, setsLabelsV) .
#	[SolC,SolL] = GREEDYSCP(C, L) if C is an array, creates a cell array SolC that is a solution of Set Cover Problem defined by C, where C{i} = S_i, an input set made by some of the elements we want to cover;
#    SolC is made by the cells of C selected by the algorithm. The elements that we want to cover are indicates by numbers from 1 to n, where n is the number of elements we want to cover;
#    therefore, C{i} is a vector of integers between 1 and n.
#
#	If C is a logical or numerical array of n rows, where C(j,i) > 0 iff element j is contained in set S_i, the output SolC will be a logical array made by the column of log(C) corresponding to the solution
#
#	If a vector L of integer labels of the elements of C is provided, SolL contains the labels corresponding to SolC. Otherwise SolL contains the positions of elements of SolC in C. SolC and SolL elements are sorted in ascending order of SolL.
#
#	This is an implementation of the well-known greedy algorithm (Chvátal, 1979), with two small modifications:
#	* In case of more than one possible choice at one step, the biggest set is chosen.
#	* Once the solution is found, we check the selected sets to find a better cover solution, removing a set if is a subset of the union of the other set.
#
#	If you use this code, please cite:
#	F. Gori, G. Folino, M.S.M. Jetten, E. Marchiori
#	"MTR: Taxonomic annotation of short metagenomic reads using clustering at multiple taxonomic ranks", Bioinformatics 2010.
#	doi = 10.1093/bioinformatics/btq649

from enum import unique
import numpy as np
import matplotlib.pyplot as plt
import numpy.matlib
# Import math Library
import math
import builtins
# import holdup
from ismember import ismember
from sympy import *
from sympy import solve, symbols, pprint


def greedy_scp(problem_params=None, V1=None, wp_c=None, uav_data=None, cfgParams=None):
    V2 = []
    T = wp_c
    V = V1
    R = problem_params['R']
    print('Aqui empieza greedy_scp')
    print('T')
    print(T)
    print('V')
    print(V)
    figG = []
    if (cfgParams['printResults']):
        vis = 'on'
    else:
        vis = 'off'

    # *=*=*=*=*
# * Input adjustment
# Get ready the SCP table without empty rows and empty columns and launch the greedy algorithm.
    ty = len(T[0])
    vy = len(V[0])
    scp_table = np.zeros((ty, vy))
    ttrip_max = uav_data['Tt']
    # Creating NEW Vertices table with the wp_c
    #for i in np.arange(1, ty+1).reshape(-1):
    for i in np.arange(0, ty).reshape(-1):
        #for j in np.arange(1, vy+1).reshape(-1):
        for j in np.arange(0, vy).reshape(-1):
            # Time Cost from base = To+(2*Tf)+Tl
            #d = np.sqrt(((T(1, i) - V(1, j)) ** 2) +
            #            ((T(2, i) - V(2, j)) ** 2))
            d = np.sqrt(((T[0][i] - V[0][j]) ** 2) + ((T[1][i] - V[1][j]) ** 2))
            # ttrip = uav_data.To + (2*round(d/uav_data.Vuav,0)) + uav_data.Tl;
# d = sqrt( ((T(1,i)-V(1,j))^2) + ((T(2,i)-V(2,j))^2));
            if (d <= problem_params['R']):
                scp_table[i, j] = 1
            else:
                scp_table[i, j] = 0

    # Building scp_table, without empty columns. Deleting the vertices which
# don't surround any waypoint
    #t = 1
    t = 0 #nuevo
    D = []

    z = 1
    #__, c = scp_table.shape
    c = len(scp_table[0])
    scp_table_s = []
    #for i in np.arange(1, c+1).reshape(-1):
    for i in np.arange(0, c).reshape(-1):
        if (0 < sum(scp_table[:, i])):
            print('scp_table_s antes')
            print(scp_table_s)
            print('scp_table....')
            print(scp_table)
            print('valor de i '+str(i))
            print('valor de t '+str(t))
            print('scp_table[:, i]')
            print(scp_table[:, i])
            scp_table_s.append(scp_table[:, i])
            print('scp_table_s despues')
            print(scp_table_s)
            t = t + 1
        else:
            D[z] = i
            z = z + 1

    # Generate an adecuate labeling of the vertices, if it has been some vertice
# deleted
    cnt = 0
    print(c)
    L = np.arange(1, c+1)
    print('vlaor de l')
    print(L)
    L_p = list()
    #for i in np.arange(1, c+1).reshape(-1):
    for i in np.arange(0, c).reshape(-1):
        #L_p[i] = L[i]
        L_p.append(L[i])
        #for k in np.arange(1, len(D)+1).reshape(-1):
        for k in np.arange(0, len(D)+1).reshape(-1): #comprobar esto........***********
            #*****************
            #*****************++
            print('vlaor de k '+str(k))
            print('vlaor de i '+str(i))
            print('valor de L')
            print(L)
            print('valor de D')
            print(D) #NO EXISTE LA D,. MIRAR EL CODIGO....
            try:
                if D[k] == L[i]:
                    L_p[i] = 0
                    cnt = cnt + 1
            except:
                 pass        

    # L_p = __builtint__.sorted(L_p) cambiado por lo de abajo
    L_p = builtins.sorted(L_p)
    #t = 1
    t = 0
    L_s = list()
    #for i in np.arange((cnt + 1), c+1).reshape(-1):
    for i in np.arange((cnt), c).reshape(-1):
        #L_s[t] = L_p(i)
        L_s.append(L_p[i])
        print('L_s')
        print(L_s)
        t = t + 1
    #
    setsCell = scp_table_s
    setsLabelsV = L_s
    # Checking first input


    print('fin greede')
    print('SolL ...')
    #print(SolL)
    print('scp_table ...')
    print(scp_table)
    print(' V2...')
    print(V2)
    print('figGr ...')
    #print(figGr)
    
    #^^^^^^^^^^^^^^^^^^^^^^^^
    #***********************
    #^^^^^^^^^^^^^^^^^^^^^^^^
    #***********************
    #aqui va el return de: 
    #return SolL,scp_table,V2,figGr
    #test para poder seguir probando el codigo:..
    V2 = [[52.286, 78.257],[95.184, 109.46]]
    SolL = [[1], [3]]
    figGr = ''
    return SolL,scp_table,V2,figGr

    #^^^^^^^^^^^^^^^^^^^^^^^^
    #***********************
    #^^^^^^^^^^^^^^^^^^^^^^^^
    #***********************


def set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset
    

    

    return cover
 

    
    return solution_setsLabelsV,scp_table,V2,figG
