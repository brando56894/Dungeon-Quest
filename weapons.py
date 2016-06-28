#!/usr/bin/python2
#~~weapons.py~~

class create(object):
    def __init__(self,name,damage):
        self.damage = damage
        self.name = name
        
    def __repr__(self):
        return self.name
