#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: cp936 -*-
import os
from os import path,system
from datetime import datetime

class AutoCrtHpp:
    def __init__(self):
        self.note = '/*!\n \
\\file:   %s\n \
\\brief:  %s\n \
\\author: wei.g iESLab\n \
\\Date:	  %s\n \
*/\n\n'

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
                    filename = ''
                    if 'HEADERS' in line:
                        filename = hfile
                    elif 'SOURCES' in line:
                        filename = cppfile
                    else:
                        fnewpro.write(line)

                    if len(filename) > 0:
                        tmp = line.replace('\n', '').strip()
                        if tmp.endswith('\\'):
                            fnewpro.write(line)
                            line = f.readline()
                            if line:
                                for i in line:
                                    if i > 'a' and i < 'z' or i > 'A' and i <'Z':
                                        pos = line.index(i)
                                        fnewpro.write(line[0:pos] + filename + ' \\\n')
                                        break
                            else:
                                fnewpro.write('\t' + filename + ' \\\n')
                            fnewpro.write(line)
                        else:
                            fnewpro.write(tmp + '\t' + filename + ' \n')

                    line = f.readline()
                f.close()
            fnewpro.close()
            os.remove(pro)
            os.rename(newPro, pro)

    def crt(self, clsname, desc):
        realCls = 'C%s' % (clsname)
        hfile = clsname.lower() + '.h'
        cppfile = clsname.lower() + '.cpp'
        with open(hfile, 'w') as f:
            f.write(self.note % (hfile, desc, datetime.now().strftime('%Y/%m/%d')))
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
            f.write(self.note % (cppfile, desc, datetime.now().strftime('%Y/%m/%d')))
            f.write('#include "%s"\n\n' % (hfile))
            f.write('%s::%s()\n{\n}\n\n' % (realCls, realCls))
            f.write('%s::~%s()\n{\n}\n' % (realCls, realCls))
            f.close()
        return hfile, cppfile

if __name__ == '__main__':
    ac = AutoCrtHpp()
    clsname = 'BreakerSchema'
    hfile, cppfile = ac.crt(clsname, '设备模型访问类')
    ac.add2pro(hfile, cppfile)
