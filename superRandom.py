#!/usr/bin/python2
#
#~superRandom.py~

from random import choice

def superRandrange(start, stop):
    randList = []
    while len(randList) != 1:
        if randList:
            randList.sort()
            start = randList[0]
            stop = randList[len(randList) - 1] + 1
        randList = list(filter(lambda x: choice([0,1]), range(start, stop)))
    return randList[0]

def superRandint(start, inclusiveStop):
    return superRandrange(start, inclusiveStop + 1)

def superChoice(array):
    return array[superRandrange(0, len(array))]

