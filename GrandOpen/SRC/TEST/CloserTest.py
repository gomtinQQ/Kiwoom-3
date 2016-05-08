# -*- coding: utf-8 -*-


def out():
    count=0
    
    def inn():
        nonlocal count
        count+=1
        return count
    return inn

if __name__ == '__main__':
    
    abs = out()
    
    print(abs())
    print(abs())
    print(abs())
    
    