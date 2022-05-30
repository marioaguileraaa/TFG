from tkinter import X, Y
import numpy as np
import sympy
import sympy as sym
# import sympy
from sympy import *
from sympy import solve, symbols, pprint

    
def foptimus(a = None,b = None,Xm = None,Ym = None,R = None): 
    #Variables of the Equation's Systems
    x,y = symbols('x,y')   
    vars = np.array([x,y])
    #Build the Line's equation between the vertice and the average
#center
    eqL = ((x - Xm(1)) / (Xm(2) - Xm(1))) == ((y - Ym(1)) / (Ym(2) - Ym(1)))
    px = []
    py = []
    for i in np.arange(1,len(a)+1).reshape(-1):
        eqC = ((((x - a(i)) ** 2) + ((y - b(i)) ** 2)) == R ** 2)
        eqns = np.array([eqC,eqL])
        solx,soly = sympy.solve(eqns,vars)
        for j in np.arange(1,len(solx)+1).reshape(-1):
            px = np.array([px,float(np.longfloat(solx(j)))])    
        for j in np.arange(1,len(soly)+1).reshape(-1):
            py = np.array([py,float(np.longfloat(soly(j)))])   
    
    #For each solution, catch the ones who cover all the waypoints
    p_x = []
    p_y = []
    for j in np.arange(1,len(px)+1).reshape(-1):
        wp_c_cnt = 0
        for k in np.arange(1,len(a)+1).reshape(-1):
            d = np.sqrt(((px(j) - a(k)) ** 2) + ((py(j) - b(k)) ** 2))
            if (np.longfloat(d) <= R):
                wp_c_cnt = wp_c_cnt + 1
        if (wp_c_cnt == len(a)):
            p_x = np.array([p_x,px(j)])
            p_y = np.array([p_y,py(j)])
    
    #For those which cover all the waypoints, select the nearest to the
#gravity center
    dmin = np.inf
    minX = np.inf
    minY = np.inf
    for j in np.arange(1,len(p_x)+1).reshape(-1):
        d = np.sqrt(((p_x(j) - Xm(2)) ** 2) + ((p_y(j) - Ym(2)) ** 2))
        if (np.longfloat(d) < dmin):
            dmin = d
            minX = p_x(j)
            minY = p_y(j)
    
    sx = minX
    sy = minY
    return sx,sy
    
    return sx,sy