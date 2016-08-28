#!/usr/bin/python2
#
#~superRandom.py~

from random import choice

#this gets really slow, at about start = 1, stop = 2500
#but i doubt we need that kind of range

def super_randrange(start, stop):
    rand_list = []
    rand_list_two = []
    r_start = start
    r_stop = stop
    while len(rand_list_two) < (r_stop - r_start):
        while len(rand_list) != 1:
            if rand_list:
                cache = rand_list
                cache.sort()
                start = cache[0]
                stop = cache[len(cache) - 1] + 1
            else:
                start = r_start
                stop = r_stop
                cache = range(start, stop)
            rand_list = list(filter(lambda x: choice([0,1]), cache))
        rand_list_two.append(rand_list[0])
        rand_list = []
    return choice(rand_list_two)

def super_randint(start, inclusive_stop):
    return super_randrange(start, inclusive_stop + 1)

def super_choice(array):
    return array[super_randrange(0, len(array))]

