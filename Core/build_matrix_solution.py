import struct
import numpy as np
    
def build_matrix_solution(ugv_path = None,uav_path1 = None,uav_path2 = None): 

    ### Build Final Solution Path for the UGV and UAV
    path_sol = []
    #for i in np.arange(1,len(ugv_path)+1).reshape(-1):
    for i in np.arange(0,len(ugv_path)).reshape(-1):
        path_sol.append({'c_ugv' : ugv_path[i],'c_uav1' : [],'c_uav2' : []})
        
    print('path_solution')
    print(path_sol)
    #Insert c_uav1 to the final path solution
    r = len(path_sol)
    u = len(uav_path1)
    for i in np.arange(0,r).reshape(-1):
        for j in np.arange(0,u).reshape(-1):
            if (path_sol[i]['c_ugv'][0] == uav_path1[j]['Coordinates'][0][0] and path_sol[i]['c_ugv'][1] == uav_path1[j]['Coordinates'][0][1]):
                path_sol[i]['c_uav1'] = uav_path1[j]['Coordinates']
    
    #Insert c_uav2 to the final path solution
    u = len(uav_path2)
    for i in np.arange(0,r).reshape(-1):
        for j in np.arange(0,u).reshape(-1):
            if (path_sol[i]['c_ugv'][0] == uav_path2[j]['Coordinates'][0][0] and path_sol[i]['c_ugv'][1] == uav_path2[j]['Coordinates'][0][1]):
                path_sol[i]['c_uav2'] = uav_path2[j]['Coordinates']
    
    print('path sol final')
    print(path_sol)
    return path_sol
    
    return path_sol