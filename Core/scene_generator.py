from cmath import pi
import random
import numpy as np
import matplotlib.pyplot as plt
    
def scene_generator(problem_params = None):   
    new_problem = problem_params
    delta = problem_params['D']
    area = problem_params['Area']
    n = problem_params['N']
    home = problem_params['Home']
    r = problem_params['R']
    groups = [[],[]]
    xy = [[],[]]
    theta = np.linspace(0,2 * pi)
    finish = False
    if (n > 0):
        if (area > 0):
            if (delta > 0):
                n_group = int(n / delta)
                while (delta > 0):

                    g = np.array([[(area * np.random.rand(1,1)[0][0])],[(area * np.random.rand(1,1)[0][0])]])
                    a = (1.5) * np.random.rand(1,1) + 0.5
                    sigma = a * r
                    h = np.random.normal(0,sigma,size=(2,n_group))
                    t = g + h
                    xy = np.concatenate((xy,t),axis=1)
                    groups = np.concatenate((groups,g),axis=1)
                    delta = delta - 1

            else:
                print('delta must be > 0')
        else:
            print('area must be > 0')
    else:
        print('n must be > 0')
    
    #Round to 3 decimals
    f = 10.0 ** 3
    #xy = np.round(f * xy) / f
    xy = np.round(xy,3)
    new_problem['T'] = xy
    
    return new_problem
    
    return new_problem