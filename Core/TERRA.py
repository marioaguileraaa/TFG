

import numpy as np
import matplotlib.pyplot as plt
# Importing the statistics module
import statistics
# Importing the statistics module
from statistics import mean
from statistics import median
# Import math Library
import math
import holdup   #para usar en vez de hold
import struct
from Voronoi_Covering_TimeOptimization import Voronoi_Covering_TimeOptimization
from greedy_scp import greedy_scp
from tsp_ga_ugv import tsp_ga_ugv
from uav_compute_path import uav_compute_path
from build_matrix_solution import build_matrix_solution
from Gravitational_Optimization import Gravitational_Optimization

    
def TERRA(cfgParams = None,problem_params = None,uav_data = None,ugv_data = None): 
    #Init Output Variables
    data_sol = []
    path_sol = []
    figures = []
    figGo = []
    V1,wp_c,figV = Voronoi_Covering_TimeOptimization(problem_params,uav_data,cfgParams)
    print('******************* Voronoi COvering time optimization: ***********')
    print('V1')
    print(V1)
    print('wp_c')
    print(wp_c)
    #print('figV')
    #print(figV)
    print('*****************  FIN VORONOI ************')


    # (2) Compute Set Covering Problem
    SolL,scp_table,V2,figGr = greedy_scp(problem_params,V1,wp_c,uav_data,cfgParams)
    print('********* INICIO GREEDY *************')
    print('SolL')
    print(SolL)
    print('scp_table')
    print(scp_table)
    print('V2')
    print(V2)
    print('figGr')
    print(figGr)
    print('***********FIN GREEDY *************')
    #Check If Home is a vertex of the solution
    Vsol = checkHome(V2,problem_params['Home'])
    if (len(problem_params['Gp'])==0):
        # (3.A) UGV's Path without Gp
        __,ugv_distance,ugv_path = tsp_ga_ugv(Vsol,ugv_data['ugv_tsp'])
        ugv_time = ugv_distance / ugv_data['Vugv']
        print('***** tsp_ga_ugv *********')
        print('ugv_distance')
        print(ugv_distance)
        print('ugv_path')
        print(ugv_path)
        print('ugv_time')
        print(ugv_time)
        print('***** FIN tsp_ga_ugv *********')
        
        # (3.B) UAV's Path without Gp
        uav_path1,uav_path2,uav_distance,uav_time,stops = uav_compute_path(wp_c,scp_table,SolL,V1,cfgParams,ugv_path,uav_data)
        print('********* uav_compute_path *******')
        print('uav_path1')
        print(uav_path1)
        print('uav_path2')
        print(uav_path2)
        print('uav_distance')
        print(uav_distance)
        print('uav_time')
        print(uav_time)
        print('stops')
        print(stops)
        print('****** FIN uah_compute_path ***********')
        #1st Solution without GOA
        total_time = ugv_time + uav_time
        total_distance = ugv_distance + uav_distance
        #s = struct('f_ugv_d',ugv_distance,'f_ugv_t',ugv_time,'f_uav_d',uav_distance,'f_uav_t',uav_time,'ftotal_d',total_distance,'ftotal_t',total_time,'stops',stops)
        s = {'f_ugv_d' : ugv_distance,'f_ugv_t' : ugv_time,'f_uav_d' : uav_distance,'f_uav_t' : uav_time,'ftotal_d' : total_distance,'ftotal_t' : total_time,'stops' : stops}
        data_sol = np.array([[data_sol],[s]])
        ####
        #AQUI PONER LAS VARIABLES DE MATLAB: 
        """
        ugv_path
          0.5          0.5
       52.286       95.184
          0.5          0.5

        uav_path1
            Coordinates: [7×2 double]

        uav_path1 coord
            52.286       95.184
                87           42
            52.286       95.184
                26          153
            52.286       95.184
                32           35
            52.286       95.184

        uav_path2
        """
        
        #################################
        ugv_path = np.array([[ 0.5, 0.5], [ 52.286,   95.184 ], [ 0.5, 0.5]])     
        uav_path1_aux =   np.array([[ 52.286,   95.184 ], [ 87,   42 ], [ 52.286,   95.184 ],[26,   153 ], [ 52.286,   95.184 ],[ 32,   35 ], [ 52.286,   95.184 ]])      
        uav_path1 = [{'Coordinates': uav_path1_aux }]
        uav_path2 = []
        ###
        #####################
        p_sol = build_matrix_solution(ugv_path,uav_path1,uav_path2)
        path_sol.append( {'path_solution': p_sol})
        print('path_sol despues')
        print(path_sol)
    else:
        # (4) GOA Execution
        if (problem_params['Gp'] == 'GravityCenter'):
            avg_x = mean(Vsol[0])
            avg_y = mean(Vsol[1])
        else:
            if (problem_params['Gp'] == 'HomeCenter'):
                avg_x = problem_params['Home'][0][0]
                avg_y = problem_params['Home'][1][0]
            else:
                if (problem_params['Gp'] == 'MedianCenter'):
                    avg_x = median(Vsol[0])
                    avg_y = median(Vsol[1])
        # (4.1) GOA
        vx_opt,vy_opt,figGo,vres = Gravitational_Optimization(problem_params,V1,avg_x,avg_y,wp_c,SolL,scp_table,cfgParams)
        # (4.2) Genetic Algorithm to UGV Path
        __,ugv_distance,ugv_path = tsp_ga_ugv(np.array([[np.array([problem_params['Home'][0][0],vx_opt])],[np.array([problem_params['Home'][1][0],vy_opt])]]),ugv_data['ugv_tsp'])
        ugv_time = ugv_distance / ugv_data['Vugv']
        # (4.3) Search Algorithm to UAV Path
        uav_path1,uav_path2,uav_distance,uav_time,stops = uav_compute_path(wp_c,scp_table,SolL,vres,cfgParams,ugv_path,uav_data)
        #i'st Solution
        total_time = ugv_time + uav_time
        total_distance = ugv_distance + uav_distance
        s = {'f_ugv_d' : ugv_distance,'f_ugv_t' : ugv_time,'f_uav_d' : uav_distance,'f_uav_t' : uav_time,'ftotal_d' : total_distance,'ftotal_t' : total_time,'stops' : stops}
        data_sol = np.array([[data_sol],[s]])
        p_sol = build_matrix_solution(ugv_path,uav_path1,uav_path2)
        path_sol = np.array([[path_sol],[{'path_solution' : p_sol}]])
    
    figR = plt.figure
    plt.plot(problem_params['T'][0],problem_params['T'][1], 'b.')
    plt.plot(problem_params['Home'][0],problem_params['Home'][1], 'k*')
    plt.plot(V2[0],V2[1], 'k+')
    plt.plot(ugv_path[:,0],ugv_path[:,1], 'g-')
    print('V2')
    print(V2)
    c = len(V2) #igual es len(V2[0])
    c_2 = c
    theta = np.linspace(0,2 * math.pi)
    c_x = list()
    c_y = list()
    for i in np.arange(0,c).reshape(-1):
        c_x.append(problem_params['R'] * np.cos(theta) + V2[0][i])
        c_y.append(problem_params['R'] * np.sin(theta) + V2[1][i])
        plt.plot(c_x[i],c_y[i],'r:')
        
    #plt.show()
    print('uav_path2')
    print(uav_path2)
    c = len(uav_path2)
    print('c')
    print(c)
    for i in np.arange(0,c).reshape(-1):
        plt.plot(uav_path2[i]['Coordinates'][:,0],uav_path2[i]['Coordinates'][:,1],'b-')
        

    plt.axis('equal')
    if (len(problem_params['Gp'])==0):
        plt.title('Final Solution without Gp')
    else:
        plt.title(np.array(['Final Solution with Gp=',problem_params['Gp']]))
    
    plt.show()
    ###
    #hsp solution:
    plt.plot(problem_params['T'][0],problem_params['T'][1], 'b.')
    #plt.plot(problem_params['Home'][0],problem_params['Home'][1], 'k*')
    plt.plot(V2[0],V2[1], 'g+')
    #plt.plot(ugv_path[:,0],ugv_path[:,1], 'g.')
    c_x = list()
    c_y = list()
    for i in np.arange(0,c_2).reshape(-1):
        c_x.append(problem_params['R'] * np.cos(theta) + V2[0][i])
        c_y.append(problem_params['R'] * np.sin(theta) + V2[1][i])
        plt.plot(c_x[i],c_y[i],'r:')
    plt.title('HSP Solution')
    plt.show()
    ########333


    #Save All figures
    figures = np.array([figures,figV,figGr,figGo,figR])
    return data_sol,path_sol,figures
    
    
def checkHome(V2 = None,Home = None): 
    #Find out if home is part of the vertices solution, in that case, put into
#the first position
    #sol_x = V2[1,:]
    #sol_y = V2[2,:]
    sol_x = V2[0]
    sol_y = V2[1]
    #home_x = Home[1,:]
    #home_y = Home[2,:]
    home_x = Home[0]
    home_y = Home[1]
    ugv_path = []
    enc = False
    #for i in np.arange(1,len(sol_x)+1).reshape(-1):
    for i in np.arange(0,len(sol_x)+0).reshape(-1):
        #if sol_x(i) == home_x and sol_y(i) == home_y:
        if sol_x[i] == home_x and sol_y[i] == home_y:
            enc = True
            pos = i
    
    if enc:
        path_x = sol_x
        path_x[pos] = path_x[0]
        path_x[0] = home_x
        path_y = sol_y
        path_y[pos] = path_y[0]
        path_y[0] = home_y
    else:
        print('home_x')
        print(home_x)
        print('sol_x')
        print(sol_x)
        path_x = list()
        for i in home_x:
            path_x.append(i)
        for i in sol_x:
            path_x.append(i)
        path_x = np.array(path_x)
        print(path_x)
        path_y = list()
        for i in home_y:
            path_y.append(i)
        for i in sol_y:
            path_y.append(i)
        path_y = np.array(path_y)
    
    ugv_path = np.array([[path_x],[path_y]])
    return ugv_path
    
    return data_sol,path_sol,figures