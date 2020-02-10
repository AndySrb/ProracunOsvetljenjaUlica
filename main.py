#!/usr/bin/env python3

import json
import math

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

class vector2F:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class vector3F:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class mesuringPoints:
    def __init__(self,x,y,a,tg,angle,cos,cos3,illuminated):
        self.x = x
        self.y = y
        self.a = a
        self.tg = tg
        self.angle = angle
        self.cos = cos
        self.cos3 = cos3
        self.illuminated = illuminated

lampIlumCarac = [] #lamp iluminacion characteristics

with open('./data.json') as json_file:
    data = json.load(json_file)
    for p in data['angle']:
        print('from: ' +  str(p['form']))
        print('to: ' +    str(p['to']))
        print('value: ' + str(p['value']))
        print('const: ' + str(p['const']))
        lampIlumCarac.append([p['form'],p['to'],p['value'],p['const']])
        print('')

lampFlow = data['lamp']['lampFlow']
bulbFlow = data['lamp']['bulbFlow']


print(lampIlumCarac)
print(lampFlow)
print(bulbFlow)

lampPos = []

for p in data['lampPos']:
    lampPos.append(vector3F(p['x'],p['y'],p['z']))


roadLenght = data['roadLenght'] #Lenght betwen 2 lamps
roadWidth = data['roadWidth']   #Road width

mesuringDotsX= roadLenght / 16  #Mesuring Dots on road lenght 
mesuringDotsY= roadWidth / 8    #Mesuring Dots on road width

x = 0
y = 0

mesuringDotsTable = []

while roadWidth >= y:
    while roadLenght >= x:
        mesuringDotsTable.append(vector2F(x,y))
        x += mesuringDotsX
    y += mesuringDotsY
    x = 0

def getValue(angle):
    form = None
    to = None
    valueHigh = None
    const = None
    valueLow = None
    if angle > 180:
        print("Error")
        exit()
    for i in lampIlumCarac:
        valueHigh = valueLow
        form = i[0]
        to = i[1]
        valueLow = i[2]
        const = i[3]
        if angle < i[1] and angle > i[0]:
            break

    if const:
        return valueLow

    return (abs((angle % form) - (to - form)) / (to - form)) * (valueHigh - valueLow) + valueLow


mathPlotDataX = []
mathPlotDataY = []
mathPlotDataZ = [0] * len(mesuringDotsTable)

for i in mesuringDotsTable:
    mathPlotDataX.append(i.x)
    mathPlotDataY.append(i.y)

finalResult = 0

for lamp in lampPos:
    print("lampX= "+str(lamp.x) + "   lampY= " + str(lamp.y))
    i = 0
    for dots in mesuringDotsTable:
        print("x=" + str(dots.x-lamp.x) + "y=" + str(dots.y-lamp.y))
        mountingHeight = lamp.z
        a=0
        if (dots.x-lamp.x) == 0 and (dots.y-lamp.y) == 0:
            a = math.sqrt(math.pow(0.001,2)+math.pow(0.001,2))
        else:
            a = math.sqrt(math.pow((dots.x-lamp.x),2)+math.pow((dots.y-lamp.y),2)) 
        
        print("a=" + str(a))

        tgAlpha = (a/mountingHeight)
        print("tg\u03B1=" + str(tgAlpha))

        angleAlpha = math.degrees(math.atan(tgAlpha))
        print("angle\u03B1=" + str(angleAlpha))

        cosAlpha =math.cos(math.radians(angleAlpha))
        print("cos\u03B1=" + str(cosAlpha))

        cos3Alpha = pow(math.cos(math.radians(angleAlpha)),3)
        print("cos3\u03B1=" + str(cos3Alpha))

        print("AngleLampCarac=" + str(getValue(angleAlpha)))
        illuminatedLampValue= getValue(angleAlpha) * ( bulbFlow / lampFlow)

        result = (illuminatedLampValue /  pow(mountingHeight,2)) * pow(math.cos(math.radians(angleAlpha)),3)
        print("Result= " + str(result))

        finalResult += result
        #dataList[i] = mesuringPoints(dots.x,dots.y,a,tgAlpha,angleAlpha,cosAlpha,cos3Alpha,result) 
        mathPlotDataZ[i] = mathPlotDataZ[i] + result
        i += 1
        print("")



finalResult = finalResult / (len(mesuringDotsTable) * len(lampPos))
print(finalResult)

f = open("results.csv", "w")
i = 0
while i < len(mesuringDotsTable):
    f.write(str(mathPlotDataX[i]) +  "," + str(mathPlotDataY[i]) + "," +  str(mathPlotDataZ[i]) + "\n")
    i = i +1
f.close()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(mathPlotDataX, mathPlotDataY, mathPlotDataZ, cmap=cm.jet, linewidth=0.2)
plt.show()




