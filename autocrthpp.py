#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: cp936 -*-
import os
from os import path,system

class AutoCrtHpp:
    def __init__(self):
        pass

    def add2pro(self, hfile, cppfile):
        pro = ''
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pro'):
                    pro = file
        if len(pro) > 0:
            newPro = pro + '.new'
            fnewpro = open(newPro, 'w')
            with open(pro, 'r') as f:
                line = f.readline()
                while line:
                    if 'HEADERS' in line:
                        fnewpro.write(line + '\t' + hfile + ' \\\n')
                    elif 'SOURCES' in line:
                        fnewpro.write(line + '\t' + cppfile + ' \\\n')
                    else:
                        fnewpro.write(line)
                    line = f.readline()
                f.close()
            fnewpro.close()
            os.remove(pro)
            os.rename(newPro, pro)

    def crt(self, clsname):
        realCls = 'C%s' % (clsname)
        hfile = clsname.lower() + '.h'
        cppfile = clsname.lower() + '.cpp'
        with open(hfile, 'w') as f:
            macro = '_%s_H' % (clsname.upper())
            f.write('#ifndef %s\n' % (macro))
            f.write('#define %s\n\n' % (macro))
            f.write('class %s\n' % (realCls))
            f.write('{\n')
            f.write('public:\n')
            f.write('\t%s();\n' % (realCls))
            f.write('\t~%s();\n' % (realCls))
            f.write('};\n\n')
            f.write('#endif // !%s\n' % (macro))
            f.close()
        with open(cppfile, 'w') as f:
            f.write('#include "%s"\n\n' % (hfile))
            f.write('%s::%s()\n{\n}\n\n' % (realCls, realCls))
            f.write('%s::~%s()\n{\n}\n' % (realCls, realCls))
            f.close()
        return hfile, cppfile

if __name__ == '__main__':
    ac = AutoCrtHpp()
    clsname = 'BreakerSchema'
    hfile, cppfile = ac.crt(clsname)
    ac.add2pro(hfile, cppfile)
