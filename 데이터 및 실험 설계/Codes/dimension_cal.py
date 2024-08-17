import math
import numpy as np

#defining all sorts of classes

class CARBONROD4_6:
    def __init__(self, name = None, length = None):
        self.length = length
        self.name = name

    def printinfo(self):
        print("Type : CARBONROD4_6")
        print("Name : ", self.name)
        print("Length : ", self.length)
class CARBONROD2 :
    def __init__(self, name = None, length = None):
        self.length = length
        self.name = name

    def printinfo(self):
        print("Type : CARBONROD2")
        print("Name : ", self.name)
        print("Length : ", self.length)

#축

CRA = CARBONROD4_6(name = "CRA")
#FRA = CARBONROD2(name = "FRA")
FARA = CARBONROD2(name = "FARA")
TVCA = CARBONROD2(name = "TVCA")
#FAFA = CARBONROD2()

#해당 설계에는 FRA와 FAFA가 존재하지 않음. 

# input data

#flapcap data
rotor_diameter  = 150
flap_wingspan = 150
flapcap_t = 2
CRA_diameter = 6
FRA_diameter = 2
FRA_Bearing_OD = 5
CRA_Bearing_OD = 10 
radial_t = 2

#이심축 데이터
rod_OD = 2
body_t = 3
radial_t = 2
pitch_length = 10

#고정부 data
stand1_AT = 43
gearAT = 10
flapcapAT = 3
s = 1
FARA_Bearing_AT = 1.5
pitcherAT = 3
flaparmAT = 1.5
endAT = 2

pitchctrlservo_AT = 10


CRA.length = stand1_AT + s + gearAT + flapcapAT + s+ flap_wingspan + s + flapcapAT
TVCA.length = CRA.length + pitchctrlservo_AT + FARA_Bearing_AT  + s + pitcherAT
FARA.length = pitcherAT + flaparmAT*4 + endAT + s*4
CRA.printinfo()
FARA.printinfo()
TVCA .printinfo()

'''
stand 고정부
s
gear+ flapcap
s
flapwingspan
s
flapcap
s
Stand고정부
//여기까지가 


TVCA의 경우

__
CRA
__
eccentric pitcher
s
4 * flaparm 
end
'''