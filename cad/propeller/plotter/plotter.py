
from math import pow, pi, atan
from scipy.optimize import brentq
d = 0.6  #pitch = 0.6 m
#o = 0.03 #parralel width = 0.03 m

def findParralelWidth(r): #function that matches my parralel width requirements
    if r <= 0.07:
        a0 = -200/49
        a1 = 4/7
        a2 = 0.01
    else:
        a0 = -100/429
        a1 = 7/429
        a2 = 0.03
    return a0 * pow(r, 2) + a1 * r + a2


def f(r, h, o):

    #print("r: " + str(r) + "\nh: " + str(h))
    #print(pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))
    return (pi * h - d * atan((pow(pow(o, 2) - pow(h, 2), 0.5))/(2 * r)))


def findroot(r, o):
    result = brentq(lambda h:f(r, h, o), 0, o)
    #print(result)
    return result

def findHoriWidth(r, h):
    return 2 * r * atan((pi * h) / d)


fullstring = ""
for i in range(1, 331):
    r = i * 0.001
    o = findParralelWidth(r)
    h = findroot(r, o)
    w = findHoriWidth(r, h)
    outputstr = str(r * 1000) + " " + str(h * 1000) + " " + str(w * 1000)
    print(outputstr + " " + str(o))
    fullstring += outputstr + "\n"


f = open("file.txt", "w+")
f.write(fullstring)
f.close()
