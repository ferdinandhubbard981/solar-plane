
from math import pow, pi, atan
from scipy.optimize import brentq
d = 0.6  #pitch = 0.6 m
#o = 0.03 #parralel width = 0.03 m

def findParralelWidth(r): #function that matches my parralel width requirements
    if r <= 0.07:
        a0 = -200/49
        a1 = 4/7
        a2 = 0.01

    elif r > 0.07 and r <= 0.32:
        a0 = -1/4
        a1 = 7/400
        a2 = 3/100

    elif r > 0.32:
        a0 = -100
        a1 = 64
        a2 = -1023/100

    return a0 * pow(r, 2) + a1 * r + a2


def f(r, h, o):

    #print("r: " + str(r) + "\nh: " + str(h))
    #print(pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))
    return (pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))


def findh(r, o):
    result = brentq(lambda h:f(r, h, o), 0, o)
    #print(result)
    return result

def findHoriWidth(r, h):
    return 2 * r * atan((pi * h) / d)

def formdatastring(r, h, w, fullstring):
    outputstr = str(w * -1000) + " " + str(r * 1000) + " " + str(h * 1000)
    print(outputstr)
    fullstring += outputstr + "\n"
    return fullstring

fullstring = ""
r = 0
o = findParralelWidth(r)
h = o
w = findHoriWidth(r, h)
fullstring = formdatastring(r, h, w, fullstring)

for i in range(1, 331):#-1 because last case is a problem in cad (it links 2 lines together which I don't want)
    r = i * 0.001
    if i == 330: #because autodesk joins 3d guide line and 2d sweep line togeter because they share a point otherwise
        o = 0.001
    else:
        o = findParralelWidth(r)
    h = findh(r, o)
    w = findHoriWidth(r, h)
    fullstring = formdatastring(r, h, w, fullstring)



f = open("file.txt", "w+")
f.write(fullstring)
f.close()
