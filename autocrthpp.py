#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: cp936 -*-
import os
from os import path,system

class AutoCrtHpp:
    def __init__(self):
        self.h = []
        self.cpp = []
        self.pro = []

    def search(self):
        for root, dirs, files in os.walk('.'):
            for file in files:
                if '.h' in file:
                    self.h.append(file)
                elif '.cpp' in file:
                    self.cpp.append(file)
                elif '.pro' in file:
                    self.pro.append(file)
        print(self.h)
        print(self.cpp)
        print(self.pro)

    def crt(self):
        clsname = 'BreakerSchema'
        hfile = clsname.lower() + '.h'
        cppfile = clsname.lower() + '.cpp'
        with open(hfile, 'w') as f:
            macro = '_%s_H\n' % (clsname.upper())
            f.write('#ifndef %s\n' % (macro))

if __name__ == '__main__':
    ac = AutoCrtHpp()
    ac.search()