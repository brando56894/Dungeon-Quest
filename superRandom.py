#!/usr/bin/python2
#
#~superRandom.py~

from random import choice

#this gets really slow, at about start = 1, stop = 2500
#but i doubt we need that kind of range

def superRandrange(start, stop):
    randList = []
    randListTwo = []
    rStart = start
    rStop = stop
    while len(randListTwo) < (rStop - rStart):
        while len(randList) != 1:
            if randList:
                cache = randList
                cache.sort()
                start = cache[0]
                stop = cache[len(cache) - 1] + 1
            else:
                start = rStart
                stop = rStop
                cache = range(start, stop)
            randList = list(filter(lambda x: choice([0,1]), cache))
        randListTwo.append(randList[0])
        randList = []
    return choice(randListTwo)

def superRandint(start, inclusiveStop):
    return superRandrange(start, inclusiveStop + 1)

def superChoice(array):
    return array[superRandrange(0, len(array))]

