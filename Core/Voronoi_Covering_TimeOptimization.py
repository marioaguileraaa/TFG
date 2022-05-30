import time
import numpy as np
import matplotlib.pyplot as plt
from enum import unique
import holdup   #para usar en vez de hold
from scipy.spatial import Voronoi, voronoi_plot_2d

# Import math Library
import math

#variable que sea global y se modifique:
uncovered_Tps   = [[], []] 
auxiliar_problemT = [[], []]
problem_aux = ''
def Voronoi_Covering_TimeOptimization(problem_params = None,uav_data = None,cfgParams = None): 
    figV = []
    #Algorithm variables
    V1 = []
    
    #print('problem_params')
    #print(problem_params)

    ### test 
    #problem_params['T'] = [[26, 87, 144, 32], [153, 42, 92, 35]]
    print('problem_params')
    print(problem_params['T'])
    problem_params_x_aux = list()
    problem_params_y_aux = list()
    for i in problem_params['T'][0]:
          problem_params_x_aux.append(i)
    for i in problem_params['T'][1]:      
          problem_params_y_aux.append(i)
    auxiliar_problemT = [problem_params_x_aux, problem_params_y_aux]
    print('auxiliar problema') 
    print(auxiliar_problemT)   
     
    ### fin test
    
    global problem_aux
    problem_aux =  problem_params
    #print('problem_aux')
    #print(problem_aux)
    #print('acabo de declarar e igualar auxiliar a problem_params[T]')
    #print(auxiliar_problemT)
    aux_i = problem_params['T']
    #uncovered_Tps = problem_params['T']
    uncovered_Tps = aux_i
    #print('linea 21 imprimo primer problem_params[T]')
    #print(problem_params['T'])
    #print('uncovered_Tps')
    #print(uncovered_Tps)
    
    covered_Tps = []
    trusted_Vertices = []
    used_vertices = []
    artificial_Vertices = problem_params['Home']
    #print('artificial_vertices')
    #print(artificial_Vertices)
    duplicates = 0
    if (cfgParams['printResults']):
        vis = 'on'
    else:
        vis = 'off'
    
    
    
    #while (not len(uncovered_Tps)==0 ): #mientras uncovered_Tps no esté vacio
    while (not len(uncovered_Tps[0])==0 ): #mientras uncovered_Tps no esté vacio

        # [STEP 1] - Calculate the Voronoi's Diagram over the WPm not covered
        nearest_vertices = [[],[]]
       
        if (not len(trusted_Vertices)==0 ): #si no está vacio trusted_vertices
            
            __,c_wp = np.size(uncovered_Tps) 
            __,c_vx = np.size(trusted_Vertices)

            
            for i in np.arange(0,c_wp).reshape(-1): #dudo en este rango...
                #print('valor de i')
                #print(i)
                #idx = 1
                #test
                idx = 0
                #test
                #fin test
                tmin = EUC_2D_Time(EUC_2D_Distance(uncovered_Tps[:,i],trusted_Vertices[:,1]),uav_data)
                #for j in np.arange(2,c_vx+1).reshape(-1):
                #print('entro en for 2')
                for j in np.arange(1,c_vx).reshape(-1): 

                    t = EUC_2D_Time(EUC_2D_Distance(uncovered_Tps[:,i],trusted_Vertices[:,j]),uav_data)
                    if (t < tmin):
                        tmin = t
                        idx = j
                
                nearest_vertices = np.append(nearest_vertices,trusted_Vertices[:,idx])
                #print('salgo de  en for 1')  
            #Delete duplicates
            #print('nearest_vertices..')
            #print(nearest_vertices)
            ####
            #unique nuevo
            listaaux2 = list()
            near_x_unique = list()
            near_y_unique = list()
            near_x = list()
            near_y = list()
            near_x = nearest_vertices[0]
            near_y = nearest_vertices[1]
            #print('nears')
            #print(near_x)
            #print(near_y)
            for i in range (0, len(near_x)):
                if ([near_x[i], near_y[i]]) in listaaux2:
                   pass
                else:
                     listaaux2.append([near_x[i], near_y[i]])
                     near_x_unique.append(near_x[i])
                     near_y_unique.append(near_y[i])
            
            #print('nears unique')
            #print(near_x_unique)
            #print(near_y_unique)
            if len(near_x_unique) >0:
             nearest_vertices = np.array([near_x_unique, near_y_unique])
            else:
             #near vertices estaba vacio...   
             pass   
            #print('nearest_vertices despues de uniques')
            #print(nearest_vertices)
            ####
            #nearest_vertices = np.transpose(unique(np.transpose(nearest_vertices),'rows'))
            #Detect duplicates and so, infinite loop in voronoi diagram
            #print('used vertices')
            #print(used_vertices)
            duplicates = isDuplicates(nearest_vertices,used_vertices)
            used_vertices = np.array([used_vertices,nearest_vertices])
        #Add these vertices to the next voronoi iteration
        #dtype=object  #por que pone que es deprecated
        #np.concatenate((xy,t),axis=1)
        #VOR_Vertices = np.array([uncovered_Tps,nearest_vertices],dtype=object)
        #print(uncovered_Tps)
        #print(nearest_vertices)
        VOR_Vertices = np.concatenate((uncovered_Tps,nearest_vertices),axis=1)
        #print(VOR_Vertices)
        #print(VOR_Vertices[1,:])
        
        #We can't do voronoi if we have 2 points (one wp and its nearest vertice)
    #or Only 2 wp and 1 v�rtice, and the distance between the WPs and their common nearest
    #vertice, is less than the R. This situation cause an infinite loop.
        #if ((len(VOR_Vertices[1,:]) == 2) or (duplicates)):
        if ((len(VOR_Vertices[0,:]) == 2) or (duplicates)):
            #m is the intermediate point between the WPs. Each iteration,
    #this vertice is nearest to the first wp
            m_x = (VOR_Vertices[0,0] + VOR_Vertices[1,2]) / 2
            m_y = (VOR_Vertices[1,0] + VOR_Vertices[1,1]) / 2
            d = EUC_2D_Distance(VOR_Vertices[:,0],np.array([[m_x],[m_y]]))
            #R = (uav_data.Tt - uav_data.To - uav_data.Tl)/2; #m
    #ttrip = EUC_2D_Time(d,uav_data);
            R = problem_params['R']
            #Rtrip = uav_data.Vuav*(uav_data.To + EUC_2D_Time(d,uav_data)*2 + uav_data.Tl); #m
            while (d > R):

                m_x = (m_x + VOR_Vertices[0,0]) / 2
                m_y = (m_y + VOR_Vertices[1,0]) / 2
                d = EUC_2D_Distance(VOR_Vertices[:,0],np.array([[m_x],[m_y]]))
                #ttrip = EUC_2D_Time(d,uav_data);

            artificial_Vertices = np.array([artificial_Vertices,np.array([[m_x],[m_y]])])
        else:
            #Create the voronoi diagram for the n iteration
            #print(VOR_Vertices)
            #print(VOR_Vertices[0,:])
            #for i in VOR_Vertices
            #VORONOI pasar (x1,xy), (x2,y2), etc que ahora tenemos (x1,x2,x3) (y1,y2,y3)

            
            #vx,vy = Voronoi(VOR_Vertices[0,:],VOR_Vertices[1,:])

            ###### FUNCION CAMBIAR ARRAY #####

            lista_futura = list()
            for i in range (0, len(VOR_Vertices[0])): 
             lista_futura.append([float(VOR_Vertices[0][i]), float(VOR_Vertices[1][i])])

            points = np.array(lista_futura)
            #print('points')
            #print(points)
            #mis POINTS ESTAN BIEN, 
            #print(VOR_Vertices)
            #print(points)
            ###### FIN FUNCION CAMBIAR ARRAY #####
            #vx,vy = Voronoi(points)
            vor = Voronoi(points)
            #print('printeamos vor vertices')
            #print(vor.vertices)
            #print(vor.vertices[0])
            #print(vor.vertices[1])
            #tiene que ser VOR.VERTICES EN VEZ DE POINTS PERO SALEN MUCHOS MENOS QUE LO QUE DEBERIA EN MATLAB.
            
            #LOS VOR.POINTS ESTAN MAL, SON LOS MISMOS QUE POINTS Y NO DEBERIA.

            vx = list()
            vy = list()
            #for i in vor.points:
            for i in vor.vertices:
                vx.append(i[0])
                vy.append(i[1])

            #print('vor points')
            #print(vor.points)
            #print('vx')
            ##print(vx)
            #print('vy')
            #print(vy)

            #comprobacion voronoi funciona con grafica
            #fig = voronoi_plot_2d(vor)
            #plt.show()
            #print(vor)
            #time.sleep(20)

            ######### finalizacionnnnn ##########3

            #print('antes trusted_vertices')
            #Delete duplicates vertices
            #trusted_Vertices = np.array([[vx[0,:]],[vy[0,:]]])
            ####
            #print('trusted antes mas antes ')
            #print(trusted_Vertices)
            listaaux = list()
            vx_unique = list()
            vy_unique = list()
            for i in range (0, len(vx)):
                if ([vx[i], vy[i]]) in listaaux:
                   pass
                else:
                     listaaux.append([vx[i], vy[i]])
                     vx_unique.append(vx[i])
                     vy_unique.append(vy[i])
            
            ####
            trusted_Vertices = np.array([vx_unique, vy_unique])
            #print('trusted despues pero antes')
            #print(trusted_Vertices)
            #print('trustedvertices')
            #print(trusted_Vertices)
            #trusted_Vertices = np.transpose(unique(np.transpose(trusted_Vertices),'rows'))
            #trusted_Vertices = np.unique(trusted_Vertices)
            #hecho con vx unique e vy unique
            #print('hola 1')
        #Add artificial vertices created in the last iteration
        #print(artificial_Vertices)
        
        #print('trusted antes')
        #print(trusted_Vertices)
        #trusted_Vertices = np.array([artificial_Vertices,trusted_Vertices]) #sumar 0.5 delante
        ###
        for i in range (0, len(artificial_Vertices[0])):
            vx_unique.insert(0, artificial_Vertices[0][i])
            vy_unique.insert(0, artificial_Vertices[1][i])
        trusted_Vertices = np.array([vx_unique, vy_unique])  

        #EN MATLAB SALEN ORDENADOS POR MENOR X LOS PUNTOS....
        # LOS ORDENO AQUI Y LUEGO VEMOS CUANDO TENGAMOS MAS PUNTOS....
        # 
        trusted_Vertices = trusted_Vertices[::, trusted_Vertices[0,].argsort()]
        print('ordenados')
        print(trusted_Vertices)


        #  
        #print(trusted_Vertices) 
        ###
        #Compute the new set of uncovered waypoints
        #print('uncovered_Tps por ahi dentro del while pero sin if ')
        #wx,wy = np.size(uncovered_Tps)
        wx = len(uncovered_Tps)
        wy = len(uncovered_Tps[0])
        #__,ct = np.size(trusted_Vertices)
        __ = len(trusted_Vertices)
        ct = len(trusted_Vertices[0])
        #print('trusted vertices despues')
        #print(trusted_Vertices)
        #print('ct')
        #print(ct)
        #print('ct')
        #print(ct)
        #print('wy')
        #print(wy)
        #for i in np.arange(1,wy+1).reshape(-1):
        #quito el + 1 porque se pasa.
        #print('antes de todoss los for covered_Tps')
        #print(covered_Tps)
        #test porque tiene mal la dimension covered-
        covered_Tps= [[],[]]
        #fin test
        V1x = list()
        V1y = list()
        for i in np.arange(0,wy).reshape(-1):
            R = problem_params['R']
            #ttrip_max = uav_data.Tt;
            best_v = -1
            tp_covered = -1
            #for j in np.arange(1,ct+1).reshape(-1):
            #quito el + 1 porque se pasa.
            for j in np.arange(0,ct).reshape(-1):
                #if (uncovered_Tps(1,i) != - 1):
                if (uncovered_Tps[0][i] != - 1):
                    #Time Cost from base = To+(2*Tf)+Tl
                    #print('antes de 2D')
                    #print('uncovered_Tps')
                    #print(uncovered_Tps)
                    #print('trusted_Vertices')
                    #print(trusted_Vertices)
                    #print('uncovered_Tps')
                    #print(uncovered_Tps[0][i])
                    #print(uncovered_Tps[1][i])
                    #print('trusted_Vertices')
                    #print(trusted_Vertices[0][j])
                    #print(trusted_Vertices[1][j])
                    d = EUC_2D_Distance([uncovered_Tps[0][i], uncovered_Tps[1][i]], [trusted_Vertices[0][j], trusted_Vertices[1][j]])
                    #d = EUC_2D_Distance(uncovered_Tps[:,i],trusted_Vertices[:,j])
                    #ttrip = uav_data.To + (2*EUC_2D_Time(d,uav_data)) + uav_data.Tl;
    #Rtrip =  uav_data.Vuav*(uav_data.To + EUC_2D_Time(d,uav_data)*2 + uav_data.Tl) ; #m
                    if (d < R and best_v != 1):
                        R = d
                        best_v = j
                        tp_covered = i
            if (best_v != - 1):
                #covered_Tps = np.array([covered_Tps,uncovered_Tps[:,tp_covered]])
                #print('covered_Tps antes')
                #print(covered_Tps)
                #print('tp_covered')
                #print(tp_covered)
                #print('uncovered_Tps ')
                #print(uncovered_Tps)
                array_aux = np.array([[uncovered_Tps[0][tp_covered]],[uncovered_Tps[1][tp_covered]]])
                covered_Tps = np.append(covered_Tps, array_aux, axis = 1)
                #deberia anadirse al final un elemento y ser un array con x e 
                #print('covered_Tps despues')
                #print(covered_Tps)
                #print('uncovered_Tps antes -1')
                #print(uncovered_Tps)
                #uncovered_Tps[:,tp_covered] = np.array([-1, -1])
                uncovered_Tps[0][tp_covered] = -1
                uncovered_Tps[1][tp_covered] = -1
                #print('uncovered por -1, -1')
                #print(uncovered_Tps)
                #AQUI NO DBEERIA SER TODO -1 SINO HABER ALGUN DATO NORMAL Y NO LO HAY EN LA ULTIMA ITERACION.

                #V1 = np.array([V1,trusted_Vertices[:,best_v]])
                #print('v1 antes de trusted_vertices')
                #print(V1)
                #print('trusted_vertices')
                #print(trusted_Vertices)
                try:
                    V1x = V1[0]
                    V1y = V1[1]
                    V1x.append(trusted_Vertices[0][best_v])
                    V1y.append(trusted_Vertices[1][best_v])
                    V1 =  [V1x, V1y]
                    print('valor V1 en linea 380 en trusted_vertices')
                    print(V1)
                except:
                    V1x.append(trusted_Vertices[0][best_v])
                    V1y.append(trusted_Vertices[1][best_v])
                    V1 =  [V1x, V1y]
                    print('valor V1 en linea 380 en trusted_vertices')
                    print(V1)   
                print('comienzzo de v1..........')
                print(V1)
                print('trusted_Vertices')
                print(trusted_Vertices)
        del_ = 0
        #for i in np.arange(1,wy+1).reshape(-1):
        #añado 1
        for i in np.arange(0,wy).reshape(-1):
            #if (uncovered_Tps(1,i) == - 1):
            """
            print('uncovered_Tps')
            print(uncovered_Tps)
            print('uncovered_Tps[i]')
            print(uncovered_Tps[0][i])
            """
            if (uncovered_Tps[0][i] == -1):
                del_ = del_ + 1
        #Update uncovered_Tps Table for the next iteration
        if (del_ > 0):
            tmp_wp_nc = uncovered_Tps
            #print('tmp_wp_nc')
            #print(tmp_wp_nc) #TIENE TODO -1 Y DEBERIA TENER UNA POSICION CON ALGO DE DATOS NORMALES...
            #print('uncovered_Tps antes de zeros')
            #print(uncovered_Tps)
            uncovered_Tps = np.zeros((wx,wy - del_))
            #print('uncovered_Tps despues de zeros')
            #print(uncovered_Tps)
            #uncovered_Tps = [[],[]] #test
            #print('uncovered_Tps despues de test')
            #print(uncovered_Tps)
            #for i in np.arange(1,wx+1).reshape(-1):
            for i in np.arange(0,wx).reshape(-1):
                #t_y = 0
                t_y = -1
                #for j in np.arange(1,wy+1).reshape(-1):
                for j in np.arange(0,wy).reshape(-1):
                    #if (tmp_wp_nc(i,j) != - 1):
                    #print('tmp_wp_nc sihape')
                    #print(str(tmp_wp_nc.shape))
                    if (tmp_wp_nc[i][j] != -1):     #aqui nunca entra y pues no acaba 
                        t_y = t_y + 1
                        #uncovered_Tps[i,t_y] = tmp_wp_nc(i,j)
                        uncovered_Tps[i][t_y] = tmp_wp_nc[i][j]
            #print('uncovered_Tpstra varios for de del mas que 0')
            #print(uncovered_Tps)
    
    #Plot Results
    #print('vis')#mio
    #print(vis)#mio
    #figLast = plt.figure('visible',vis)
    figLast = plt.figure()#mio
    #figLast['Name'] = 'Voronoi_Solution'
    figLast.suptitle('Voronoi_Solution') #mio
    if (cfgParams['saveResults']):
        figV = np.array([figV,figLast])
    
    #hold('on')
    #holdup('on') #comentado por mi.
    #print('problem_paramsT en auxiliar')
    #print(auxiliar_problemT)
    #print('problem_params')
    #print(problem_params)
   # print('problem_params[T][0,:]')
    #print(problem_params['T'][0])
    #print('v1')
    #print(V1)
    #v1 ESTA MAL, DBEERIA SER DOS DIMENSIONES CON PUNTOS...
    #print(V1[0])
    #print(V1[1])
    #plt.plot(problem_params['T'][0,:],problem_params['T'][1,:],'blue.',V1[0,:],V1[1,:],'green+')



    #TEST
    #problem_params['T'] = [[26, 87, 144, 32], [153, 42, 92, 35]] #para pruebas
    problem_params['T'] = auxiliar_problemT  #para uso real.
    
    #print('problems params[T] falsificado')
    #FIN TEST

    #MIRAR EN INTERNET Y COMPARAR CON MATLAB....
    #plt.plot(problem_params['T'][0],problem_params['T'][1])
    #plt.show()
    #plt.plot(V1[0],V1[1])
    #plt.show()
    plt.plot(problem_params['T'][0],problem_params['T'][1],'b.',V1[0],V1[1],'g+')
    #MIRAR EN INTERNET Y COMPARAR CON MATLAB....
    #__,c = V1.shape
    c = len(V1[0])
    
    theta = np.linspace(0,2 * math.pi)
    c_x = list()
    c_y = list()
    #for i in np.arange(1,c+1).reshape(-1):
    for i in np.arange(0,c).reshape(-1):
        #tiene pinta de cambiar los (,) por [][] minimo.
        #c_x[i,:] = problem_params['R'] * np.cos(theta) + V1(1,i)
        #c_y[i,:] = problem_params['R'] * np.sin(theta) + V1(2,i)
        
        c_x.append(problem_params['R'] * np.cos(theta) + V1[0][i])
        c_y.append(problem_params['R'] * np.sin(theta) + V1[1][i])
        #print(' problem_params['R'] * np.cos(theta) + V1[0][i]\n\n')
        #print( problem_params['R'] * np.cos(theta) + V1[0][i])
        #print('c_x i')
        #print(c_x[i])
        #MIRAR EN INTERNET Y COMPARAR CON MATLAB....
        #plt.plot(c_x[i,:],c_y[i,:],'r:')
        plt.plot(c_x[i],c_y[i],'r:') #nuevo
        #plt.show()
        #MIRAR EN INTERNET Y COMPARAR CON MATLAB....
    
    
    #holdup('off')
    #hold('off')
    plt.axis('equal')
    plt.show()
    plt.title('Voronoi Solution')
    
    print('V1 final voronoi')
    print(V1)
    return V1,covered_Tps,figV
    
    # Search duplicates between two vectors
    
def isDuplicates(lA = None,lB = None): 
    bool = False
    #Count duplicates and so, infinite loop in voronoi diagram
    #print(lA)
    #print(lB)
    #__,lv = lA.shape
    #__,lu = lB.shape
    __,lv = np.size(lA)
    __,lu = np.size(lB)
    
    
    #for i in np.arange(1,lv+1).reshape(-1):
    for i in np.arange(0,lv).reshape(-1):
        for j in np.arange(1,lu+1).reshape(-1):
            if (lA[:,i] == lB[:,j]):
                bool = True
                break
    
    return bool
    
    
def EUC_2D_Distance(last = None,next = None): 
    #d = np.sqrt(((last(1,1) - next(1,1)) ** 2) + ((last(2,1) - next(2,1)) ** 2))
    d = np.sqrt(((last[0] - next[0]) ** 2) + ((last[1] - next[1]) ** 2))
    d = np.round(d,4)
    return d
    
    
def EUC_2D_Time(d = None,uav_data = None): 
    t = np.round(d / uav_data['Vuav'],0)
    return t
    
    return V1,covered_Tps,figV