import numpy as np
#from ..Core.foptimus import foptimus
import foptimus
    
def Gravitational_Optimization(problem_params = None,V1 = None,avg_x = None,avg_y = None,wp_c = None,SolL = None,scp_table = None,cfgParams = None): 
    #This algorithm optimizes the UGV path for the FCURP-MRS
    figG = []
    vres = np.zeros((2,len(V1[1,:])))
    wp_c_aux = wp_c
    r,c = scp_table.shape
    vx_opt = []
    vy_opt = []
    #theta = linspace(0,2*pi);
    
    for i in np.arange(1,c+1).reshape(-1):
        for k in np.arange(1,len(SolL)+1).reshape(-1):
            a = []
            b = []
            if (i == SolL(k) and V1(1,i) != problem_params.Home[1,:] and V1(2,i) != problem_params.Home[2,:]):
                Xm = np.array([V1(1,i),avg_x])
                Ym = np.array([V1(2,i),avg_y])
                if (V1(1,i) != avg_x and V1(2,i) != avg_y):
                    for j in np.arange(1,r+1).reshape(-1):
                        if (scp_table(j,i) == 1 and wp_c_aux(1,j) != - 1):
                            a = np.array([a,wp_c(1,j)])
                            b = np.array([b,wp_c(2,j)])
                            wp_c_aux[1,j] = - 1
                    sx,sy = foptimus(a,b,Xm,Ym,problem_params.R)
                else:
                    sx = V1(1,i)
                    sy = V1(2,i)
                vx_opt = np.array([vx_opt,sx])
                vy_opt = np.array([vy_opt,sy])
                vres[:,i] = np.array([[sx],[sy]])
            else:
                if (i == SolL(k) and V1(1,i) == problem_params.Home(1,1) and V1(2,i) == problem_params.Home(2,1)):
                    vres[:,i] = np.array([[V1(1,i)],[V1(2,i)]])
    
    return vx_opt,vy_opt,figG,vres
    
    return vx_opt,vy_opt,figG,vres