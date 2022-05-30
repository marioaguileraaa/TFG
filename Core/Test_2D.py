# function [solution] = Test_2D(problem_params, dana_params, cfgParams)
#  This function tests TERRA2D for a particular ECU-CSURP scenario
#  Inputs:
#    problem_params - ECU_CSURP Parameters
#    uav_data       - data info of the uav
#    ugv_data       - data info of the ugv
#    cfgParams      - Configuration Parameters of the Test
#  Outputs:
#    solution       - struct with the ouput parameters
from multiprocessing.pool import CLOSE
from os import mkdir
from tkinter import mainloop
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import struct
#import sys
import time
#import scene_generator
#from ..Launcher.scene_generator import scene_generator
from scene_generator import scene_generator
#sys.path.insert(1, '../Core/')
#from ..Core.TERRA import TERRA
from TERRA import TERRA
from pandas import *

def DatosCSV(ficheroCsv):
    print('accediendo al fichero csv '+ficheroCsv)
    #en la primera columna los puntos en las coord X, 
    #en la segunda columna los puntos en las coord Y, 
    #en la tercera columna el número de puntos. 
    data = read_csv(ficheroCsv)
    
    coor_x = data['CoordX'].tolist()
    coor_y = data['CoordY'].tolist()
    Num_puntos = data['Num_puntos'].tolist()
    #problem_params_T = [[26,87, 144, 32],[153, 42, 92, 35]];
    problem_params_T = [coor_x, coor_y];
    problem_params_N = int(Num_puntos[0])
    print('problem_params_T')
    print(problem_params_T)
    print('problem_params_N')
    print(problem_params_N)

    return problem_params_T, problem_params_N


def Test_2D(problem_params = None,uav_data = None,ugv_data = None,cfgParams = None): 
    cnt = 1
    solution = []
    for i in np.arange(1,cfgParams['iterations']+1).reshape(-1):
        #Create save dir for the results of this iteration
        #itdir = np.array([cfgParams['saveDir'],'It-',str(cnt),cfgParams['slash']])
        itdir = cfgParams['saveDir']+cfgParams['slash']+'It-'+str(cnt)+cfgParams['slash']
        #print(itdir)
        mkdir(itdir)
        # Generate Random 2D Scenario
        problem_params = scene_generator(problem_params)   
        #problem_params['T'] = [[26,87, 144, 32],[153, 42, 92, 35]];
        #problem_params['N'] = 4; 
        #leyendo de un csv:
        problem_params['T'], problem_params['N'] = DatosCSV('D:\TERRA\Core\FicheroDatosEntradaTerra.csv')
        
        # Yu. et al (2018) Random Generator
#[problem_params] = graphMakingNew([300 0 110 0], 1, problem_params);
        print(np.array(['Computing solution for Scenario ',str(cnt),' ...']))
        t = time.time()
        data_sol,path_sol,figures = TERRA(cfgParams,problem_params,uav_data,ugv_data)
        tc = time.time() - t
        #Saving
        if (cfgParams['saveResults']):
            solution = saveResults(cfgParams,tc,data_sol,path_sol,problem_params,uav_data,ugv_data,figures,itdir)
        print(np.array(['Execution ',str(cnt),' completed.']))
        cnt = cnt + 1
    
    #Simulation Stage
    if (cfgParams.Vrep):
        mainloop(path_sol(1).path_solution)
    
    return solution
    
    #This function stacks the iteration output to the general output, and also, save
#the iteration output
    
def saveResults(cfgParams = None,tc = None,data_sol = None,path_sol = None,problem_params = None,uav_data = None,ugv_data = None,figures = None,itdir = None): 
    print('Saving results ...')
    # Init solution struct
#  cT      - array of the computational time taken by TERRA to compute a solution
#  dataRes - array of the computational results of the TERRA execution (see definition in TERRA3D.m)
#  pathRes - array of the UGV-UAV path planning solution of TERRA
    solution = {'cT' : [],'dataRes' : [],'pathRes' : []}
    #Stacking
    solution['cT'] = tc
    solution['dataRes'] = {'It' : data_sol}
    solution['pathRes'] = {'It' : path_sol}
    #Saving Data
    fpath = np.array([itdir,'data.mat'])
    #np.save(fpath,'tc','data_sol','path_sol','problem_params','uav_data','ugv_data','cfgParams')
    #Saving Figures
    if (not len(figures)==0 ):
        __,c = figures.shape
        for i in np.arange(1,c+1).reshape(-1):
            name = np.array([itdir,figures(i).Name,'.fig'])
            plt.figure(figures(i))
            plt.savefig(name)
    
    if (not cfgParams['printResults'] ):
        CLOSE('all')
    
    return solution
    
    return solution