# -*- coding: utf-8 -*-

import logging


def test1():
    dd=Toy()
    dd.setToy("airPlane")
    
    print(dd.getToy())
    
class Toy():
    
    def setToy(self,toy):
        self.toy=toy
        
    def getToy(self):
        return self.toy
    
    
if __name__ == '__main__':
    
    test1()