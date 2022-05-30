import numpy as np
import struct
import search_uav_operations
import search_uav_path
    
def uav_compute_path(wp_c = None,scp_table = None,SolL = None,Vsol = None,cfgParams = None,ugv_path = None,uav_data = None): 
    #uav_compute_path(xyS, routeS, home_x, home_y, x, y, wp_c, scp_table, SolL, v_op, showResults, ugv_path, uav_data, type, saveResults, fullname)
    uav_path1 = []
    uav_path2 = []
    uav_path1_coord = []
    stops = 0
    distance = 0
    time = 0
    wp_c_aux = wp_c
    #r,c = scp_table.shape
    c = len(scp_table[0])
    r = len(scp_table)
    
    #TODO PERFECTO HASTA AQUI...
    #for i in np.arange(1,c+1).reshape(-1):
    for i in np.arange(0,c).reshape(-1):
        #for k in np.arange(1,len(SolL)+1).reshape(-1):
        for k in np.arange(0,len(SolL)).reshape(-1):
            #if (i == SolL(k)):
            print('k es '+str(k))
            if (i == SolL[k]):
                subpath = np.array([[Vsol[0][i]],[Vsol[1][i]]])
                #nuevo
                subpath_aux_x = subpath[0]
                subpath_aux_y = subpath[1]
                #fin nuevo
                #for j in np.arange(1,r+1).reshape(-1):
                for j in np.arange(0,r).reshape(-1):
                    #if (scp_table[j][i] == 1 and wp_c_aux[1][j] != - 1):
                    if (scp_table[j][i] == 1 and wp_c_aux[0][j] != - 1):
                        #subpath = np.array([subpath,np.array([[wp_c[0][j]],[wp_c[1][j]]])])
                        
                        subpath_aux_x = np.concatenate(( subpath_aux_x, np.array([wp_c[0][j]]) ))
                        subpath_aux_y = np.concatenate(( subpath_aux_y, np.array([wp_c[1][j]]) ))
                        #subpath = np.concatenate(( subpath, np.array([[wp_c[0][j]],[wp_c[1][j]]]) ))
                        subpath = np.array([subpath_aux_x, subpath_aux_y])
                        print('subpath despues')
                        print(subpath)
                        
                        wp_c_aux[0][j] = - 1
                # DISTANCE BASED SEARCHING
                #[rteP, dis, st] = search_uav_path( subpath, uav_data);
                print('*****antes de search uav path*********')
                #print('subpath')
                #print(subpath) #bien
                #print('uav_data')
                #print(uav_data) #bien
                [rteP, dis, st] = search_uav_path.search_uav_path( subpath, uav_data)
                print('dis de search_uav_path')
                print(dis)

                # TIME BASED SEARCHING
                #rteT,dis,t,st = search_uav_operations(subpath,uav_data,cfgParams)
                #time = time + t

                print('*****************')
                print('*****************')
                print('*****************')

                distance = distance + dis
                stops = stops + st
                #UAV Path for Distance-Based Searching or Time-Based Searching
                
                ru = len(ugv_path)
                #for z in np.arange(1,ru+1).reshape(-1):
                for z in np.arange(0,ru).reshape(-1):
                    
                    #if (ugv_path[z,:] == np.transpose(Vsol[:,i])):
                    if np.round(ugv_path[z][0], 1) == np.round(Vsol[0][i], 1)  and np.round(ugv_path[z][1], 1)  == np.round(Vsol[1][i], 1) :
                        #print('iguales')
                    
                        xy_uav = np.array([np.transpose(subpath[0]),np.transpose(subpath[1])])
                        print('xy_uav')
                        print(xy_uav)
                        # DISTANCE BASED SEARCHING
                        #esto es un append o concatenate de manual...
                        
                        

                        aux = [xy_uav[0][rteP], xy_uav[1][rteP]]
                        print('aux coord')
                        print(aux)
                        struc_aux = {'Coordinates': aux }
                        
                        uav_path1_coord.append(aux)
                        


                        # TIME BASED SEARCHING
                        # uav_path2 = np.array([uav_path2,{'Coordinates' : np.array([xy_uav(rteT,1),xy_uav(rteT,2)])}])
    #mio 
    struc_aux = {'Coordinates': uav_path1_coord }
    uav_path1.append(struc_aux)
    print(uav_path1)

    #mio



    ### START Drawing
    if (cfgParams['printResults']):
        pass
    
    ### STOP Drawing
    
    return uav_path1,uav_path2,distance,time,stops
    
    return uav_path1,uav_path2,distance,time,stops