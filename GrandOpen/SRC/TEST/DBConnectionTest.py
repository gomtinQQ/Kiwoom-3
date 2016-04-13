# -*- coding: utf-8 -*-
import sqlite3


def test():
    return  sqlite3.connect("../DATABASE/VolumeForeignCompany")
    
    
    
    
    
if __name__ == '__main__':
    
    
    conn = []
    for connections in range(10):
        conn.append(test()) 
    
    for i in conn:
        print(i.cursor())