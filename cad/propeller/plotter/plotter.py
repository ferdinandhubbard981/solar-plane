
from math import pow, pi, atan
from scipy.optimize import brentq
#all units in metres except for final output
widthoffset = 0*0.001
hoffset = 0*0.001
elongate = False
extsurface = True
extsurfaceconst = (15+7.5)*0.001
d = 0.6  #pitch = 0.6 m
multiplier = 0.5 #based on position of sweep path
initialwidth = 0.015
#o = 0.03 #parralel width = 0.03 m
ispatch = True
ismultipliedsurface = False
surfacemultiplier = 1
surfacepwidthconst = 50 * 0.001
ismirror = True
proplength = 0.66 #(m)
def quardraticFunction(input, a0, a1, a2):
    return a0 * pow(input, 2) + a1 * input + a2
def findParralelWidth(r): #function that matches my parralel width requirements
    if r <= 0.02:
        pwidth = 15 * 0.001 #for connection between two bades
    #elif r > 0.02 and r < 0.04:
    #    return findParralelWidth(0.02) + (findParralelWidth(0.04) - findParralelWidth(0.02)) * (r - 0.02)/(0.04 - 0.02)
    elif r > 0.02 and r <= 0.07:

        a0 = -8
        a1 = 28/25
        a2 = -23/2500
        pwidth = quardraticFunction(r, a0, a1, a2)

    elif r > 0.07 and r <= 0.32:
        a0 = -1/4
        a1 = 7/400
        a2 = 3/100
        pwidth = quardraticFunction(r, a0, a1, a2)

    elif r > 0.32:
        a0 = -100
        a1 = 64
        a2 = -1023/100
        pwidth = quardraticFunction(r, a0, a1, a2)

    pwidth *= multiplier
    return pwidth


def f(r, h, o):

    #print("r: " + str(r) + "\nh: " + str(h))
    #print(pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))
    return (pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))


def findh(r, o):
    if r <= 0.02:
        hval = 0
    elif r > 0.02 and r < 0.04:
        hval = findh(0.04, o) * (r - 0.02)/(0.04 - 0.02)
    else:
        hval = brentq(lambda h:f(r, h, o), 0, o)

    #print(hval)
    return hval

def findHoriWidth(r, h, o):
    #if r > 0.02 and r < 0.04:

        #width =  2 * r * atan((pi * h) / d) #based on r and h (from custom equations)
    #else:

    width = pow(pow(o, 2) - pow(h, 2), 0.5) #based on o and h using pythagoras
    if r < 0.07 and width <= initialwidth * multiplier:
        width = initialwidth * multiplier #when rail is in center of profile
    return width;

def formdatastring(r, h, w):
    outputstr = str(w * -1000) + " " + str(r * 1000) + " " + str(h * 1000)
    print(outputstr)
    return outputstr

def writeToFile(file, data): #file is opened file. data is array of strings
    for i in range(len(data)):
        file.write(data[i] + "\n")

def doStep(i):
    r = i * 0.001

    if i > 330:
        r = 330 * 0.001
    if r == 330 * 0.001: #because autodesk joins 3d guide line and 2d sweep line togeter because they share a point otherwise
        o = 0.0002 * multiplier
    else:
        o = findParralelWidth(r)

    h = findh(r, o)

    if i == 0:
        h = 0

    w = findHoriWidth(r, h, o)
    if ismultipliedsurface:
        surfacemultiplier = surfacepwidthconst/o

    if ismultipliedsurface:
        h *= surfacemultiplier
        w *= surfacemultiplier
    if extsurface:
        w += extsurfaceconst
    #print(str(w) + "\n")
    w += widthoffset
    if i > 330:
        r = i * 0.001
    if ismirror:
        mirror0.append(formdatastring(r, h+hoffset, w))
        #if h != 0 or (w != initialwidth/2 and w != -1*initialwidth/2):
        mirror1.append(formdatastring(r, h*-1+hoffset, -w)) #initialwidth - w for reverse

        if r != 0 or h != 0:
            mirror2.append(formdatastring(r*-1, h*-1+hoffset, w))
        if r != 0 or (w != initialwidth/2 and w != -1*initialwidth/2):
            mirror3.append(formdatastring(r*-1, h+hoffset, -w))
    else:
        fullstring.append(formdatastring(r, h, w))


fullstring = []
mirror0 = []
mirror1 = []
mirror2 = []
mirror3 = []

length = 0
if elongate:
    length = int(proplength*1000/2 + 1 + 50)
else:
    length = int(proplength*1000/2 + 1)

for i in range(0, length):#-1 because last case is a problem in cad (it links 2 lines together which I don't want)
    doStep(i)


if ispatch:
    filename = "surface.txt"
    if extsurface:
        filename = "extsurface.txt"
    f = open(filename, "w+")
    writeToFile(f, mirror0)
    writeToFile(f, mirror1[::-1])
    writeToFile(f, mirror3)
    writeToFile(f, mirror2[::-1])
    f.close()
else:

    f = open("mirror1.txt", "w+")
    writeToFile(f, mirror1)
    f.close()
    f = open("mirror2.txt", "w+")
    writeToFile(f, mirror3)
    f.close()

    f = open("mirror3.txt", "w+")
    writeToFile(f, mirror2)
    f.close()
    f = open("mirror4.txt", "w+")
    writeToFile(f, mirror0)
    f.close()

f = open("file.txt", "w+")
writeToFile(f, fullstring)
f.close()
