import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
    
def Voronoi_Covering_Optimization_nearVertex(problem_params = None,cfgParams = None): 
    #VORONOI_COVERING_OPTIMIZATION Summary of this function goes here
#   This function uses the voronoi diagram to optimize the problem of
#   covering all the waypoints received in the problem.
    figV = []
    #Algorithm variables
    V1 = []
    wp_c = []
    vx_p = []
    vy_p = []
    duplicates = 0
    near_wd = []
    wp_c_cnt = 0
    wp_nc = problem_params.T
    wp_nc_cnt = len(wp_nc[1,:])
    art_vert = problem_params.Home
    R = problem_params.R
    v_used = []
    vx_sol = []
    vy_sol = []
   
    
    while (0 < wp_nc_cnt):

        # [STEP 1] - Calculate the Voronoi's Diagram over the WPm not covered
        if (not len(vx_p)==0 ):
            #Search and catch the nearest vertice to each wp_nc and add to
#near_v
            __,c_wp = wp_nc.shape
            __,c_vx = vx_p.shape
            near_v = []
            t = 1
            dminT = np.inf
            for i in np.arange(1,c_wp+1).reshape(-1):
                dmin = np.sqrt(((wp_nc(1,i) - vx_p(1)) ** 2) + ((wp_nc(2,i) - vy_p(1)) ** 2))
                near_v[1,i] = vx_p(1)
                near_v[2,i] = vy_p(1)
                for j in np.arange(1,c_vx+1).reshape(-1):
                    d = np.sqrt(((wp_nc(1,i) - vx_p(j)) ** 2) + ((wp_nc(2,i) - vy_p(j)) ** 2))
                    if (d < dmin):
                        dmin = d
                        near_v[1,t] = vx_p(j)
                        near_v[2,t] = vy_p(j)
                        t = t + 1
                if (dmin < dminT):
                    dminT = dmin
            #Delete duplicates in near_v and add them to near_wd
            near_wd = np.array([[0],[0]])
            __,c_nearv = near_v.shape
            t = 1
            for i in np.arange(1,c_nearv+1).reshape(-1):
                val = near_v[:,i]
                in_ = 0
                j = 1
                while (j <= len(near_wd[1,:])):

                    if (val == near_wd[:,j]):
                        in_ = in_ + 1
                    j = j + 1

                if (0 == in_):
                    near_wd[:,t] = val
                    t = t + 1
            __,lv = near_wd.shape
            __,lu = v_used.shape
            #Detect duplicates and so, infinite loop in voronoi diagram
            duplicates = 0
            for i in np.arange(1,lv+1).reshape(-1):
                for j in np.arange(1,lu+1).reshape(-1):
                    if (near_wd[:,i] == v_used[:,j]):
                        duplicates = duplicates + 1
            v_used = np.array([v_used,near_wd])
        #Add these vertices to the next voronoi iteration
        wp_plus_v = np.array([wp_nc,near_wd])
        #We can't do voronoi if we have 2 points (one wp and its nearest vertice)
#or Only 2 wp and 1 v�rtice, and the distance between the WPs and their common nearest
#vertice, is less than the R. This situation cause an infinite loop.
        if ((len(wp_plus_v[1,:]) == 2) or (duplicates > 0)):
            #m is the intermediate point between the WPs. Each iteration,
#this vertice is nearest to the first wp
            m_x = (wp_plus_v(1,1) + wp_plus_v(1,2)) / 2
            m_y = (wp_plus_v(2,1) + wp_plus_v(2,2)) / 2
            d = np.sqrt(((wp_plus_v(1,1) - m_x) ** 2) + ((wp_plus_v(2,1) - m_y) ** 2))
            while (d > R):

                m_x = (m_x + wp_plus_v(1,1)) / 2
                m_y = (m_y + wp_plus_v(2,1)) / 2
                d = np.sqrt(((wp_plus_v(1,1) - m_x) ** 2) + ((wp_plus_v(2,1) - m_y) ** 2))

            art_vert = np.array([art_vert,np.array([[m_x],[m_y]])])
        else:
            #Create the voronoi diagram for the n iteration

            #convertir a lista de tublas
            vx,vy = Voronoi(wp_plus_v[1,:],wp_plus_v[2,:])
            #Delete duplicates vertices
            p = 1
            vertices = np.array([[vx[1,:]],[vy[1,:]]])
            vertices_s = np.array([[0],[0]])
            for i in np.arange(1,len(vertices)+1).reshape(-1):
                v = vertices[:,i]
                in_ = 0
                __,c = vertices_s.shape
                for j in np.arange(1,c+1).reshape(-1):
                    if (v == vertices_s[:,j]):
                        in_ = in_ + 1
                if in_ == 0:
                    vertices_s[:,p] = v
                    p = p + 1
            vx_p = vertices_s[1,:]
            vy_p = vertices_s[2,:]
        #Add artificial vertices created in the last iteration
        vx_p = np.array([art_vert[1,:],vx_p])
        vy_p = np.array([art_vert[2,:],vy_p])
        #Compute the new set of uncovered waypoints
        wx,wy = wp_nc.shape
        for i in np.arange(1,wy+1).reshape(-1):
            dmin = R
            best_v = - 1
            wp_v = - 1
            for j in np.arange(1,len(vx_p)+1).reshape(-1):
                if (wp_nc(1,i) != - 1):
                    d = np.sqrt(((wp_nc(1,i) - vx_p(j)) ** 2) + ((wp_nc(2,i) - vy_p(j)) ** 2))
                    if (d < dmin and best_v != 1):
                        dmin = d
                        best_v = j
                        wp_v = i
            #Actualizar tablas con el v�rtice de la m�nima distancia al wp_nc
# The Waypoint wp_nc(x,i) was covered by unless one vertice!!
            if (best_v != - 1):
                wp_c_cnt = wp_c_cnt + 1
                wp_c[1,wp_c_cnt] = wp_nc(1,wp_v)
                wp_c[2,wp_c_cnt] = wp_nc(2,wp_v)
                vx_sol[1,wp_c_cnt] = vx_p(best_v)
                vy_sol[1,wp_c_cnt] = vy_p(best_v)
                #fprintf('Waypoint[#.4f,#.4f] - V�rtice[#.4f,#.4f]',wp_nc(1,wp_v),wp_nc(2,wp_v),vx_p(best_v),vy_p(best_v));
#fprintf('\n');
                wp_nc[1,wp_v] = - 1
                wp_nc[2,wp_v] = - 1
                wp_nc_cnt = wp_nc_cnt - 1
        del_ = 0
        for i in np.arange(1,wy+1).reshape(-1):
            if (wp_nc(1,i) == - 1):
                del_ = del_ + 1
        #Update wp_nc Table for the next iteration
        if (del_ > 0):
            tmp_wp_nc = wp_nc
            wp_nc = np.zeros((wx,wy - del_))
            for i in np.arange(1,wx+1).reshape(-1):
                t_y = 0
                for j in np.arange(1,wy+1).reshape(-1):
                    if (tmp_wp_nc(i,j) != - 1):
                        t_y = t_y + 1
                        wp_nc[i,t_y] = tmp_wp_nc(i,j)

    
    V1 = np.array([[vx_sol],[vy_sol]])
   
    
    return V1,wp_c,figV
    
    return V1,wp_c,figV