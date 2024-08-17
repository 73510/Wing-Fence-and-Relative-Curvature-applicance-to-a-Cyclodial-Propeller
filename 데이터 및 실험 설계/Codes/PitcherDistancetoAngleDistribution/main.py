import math
import numpy as np

degrees = np.arange(0, 360, step =1)

pitcherdistance = 6
FRAtoFAFA = 20

rotorradius = 75


#x축 기준으로 degree 잡음, Degree는 Mainframe의 각도. 

degreemapx = []
degreemapy = []

for degree in degrees : 
    
    degstep = 0.1
    A = (rotorradius * np.cos(np.radians(degree)) ,rotorradius * np.sin(np.radians(degree)))

    mindeg = -1
    mindiff = 1000000
    for searchdeg in np.arange(degree, degree + 90, step =degstep) : 

        B  = (rotorradius * np.cos(np.radians(searchdeg)) ,rotorradius * np.sin(np.radians(searchdeg))-pitcherdistance)

        dist = ((A[0] - B[0])**2 + (A[1] - B[1])**2)**(0.5)

        diff = abs(dist - FRAtoFAFA)

        if (mindiff > diff) :
            mindiff = diff
            mindeg = searchdeg
    B  = (rotorradius * np.cos(np.radians(mindeg)) ,rotorradius * np.sin(np.radians(mindeg))-pitcherdistance)
    기준deg = degree + 90
    vecFRAtoFAFA = [B[0]-A[0], B[1]-A[1]]
    degreeFRAtoFAFA = np.degrees(np.arctan(vecFRAtoFAFA[1]/vecFRAtoFAFA[0]))
    degraw = (degreeFRAtoFAFA - 기준deg)%180
    if (degraw >=90) : 
        degraw -= 180
    

    
    degreemapx.append(degree)
    degreemapy.append(degraw)



with open('output.csv', mode ='w') as f:
    for i in range(len(degreemapx)):
        print(degreemapx[i], degreemapy[i], sep = ',', end = '\n')
        f.write(str(degreemapx[i]) +','+ str(degreemapy[i]) + '\n')