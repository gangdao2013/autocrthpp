#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: cp936 -*-
import os
from os import path, system
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox

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
                    elif 'SOURCES' in line and 'RESOURCE' not in line:
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
        if os.path.exists(hfile) or os.path.exists(cppfile):
            return False, hfile, cppfile
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
        return True, hfile, cppfile

class mainWin(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('180x200+400+200')
        super().__init__()
        self.clsname = tk.StringVar()
        self.clsdesc = tk.StringVar()
        self.pack()
        self.main_window()
        self.root.mainloop()
    def main_window(self):
        tk.Label(self.root, text='类名称:', font=('Arial', 12)).pack(anchor=W)
        tk.Entry(self.root, textvariable=self.clsname).pack(anchor=W)
        tk.Label(self.root, text='类描述:', font=('Arial', 12)).pack(anchor=W)
        tk.Entry(self.root, textvariable=self.clsdesc).pack(anchor=W)
        tk.Button(self.root, text='创建', command=self.onOk, fg='white', bg='black',
                  activeforeground='white', activebackground='navy', width=8, height=1)\
            .pack(side=LEFT, anchor=W)
        tk.Button(self.root, text='退出', command=self.root.quit, fg='white', bg='black',
                  activeforeground='white', activebackground='red', width=8, height=1)\
            .pack(side=RIGHT, anchor=W)
    def onOk(self):
        clsname = self.clsname.get()
        if len(clsname) == 0:
            messagebox.showerror(title='error', message='类名不能为空.')
        else:
            ac = AutoCrtHpp()
            result, hfile, cppfile = ac.crt(clsname, self.clsdesc.get())
            if result:
                ac.add2pro(hfile, cppfile)
                os.system('qmake_vc.bat')
                messagebox.showinfo(title='ok', message='已创建')
            else:
                messagebox.showinfo(title='ok', message='类文件已存在，不能创建')


if __name__ == '__main__':
    mainWin()