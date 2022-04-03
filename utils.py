import os, glob
from fnmatch import fnmatch
from PyQt5.QtWidgets import QFileDialog, QMessageBox

root = '.\\'
pattern = 'SA_summary.dat'
newSA = 'Col_SA_summary.dat'

def mergeSA(fld, file):
   fcnt = int(0)
#    with open(newSA,'w') as outfile:
   with open(file,'w') as outfile:
      for path, subdirs, files in os.walk(fld):
         for name in files:
            if fnmatch(name, pattern):
               fname = os.path.join(path, name)
               fcnt = fcnt + 1
               print(fname)
               with open(fname) as infile:
                  if fcnt < 2:
                     outfile.write(infile.read())
                  else:
                     next(infile)
                     outfile.write(infile.read())


def getfilist(fld, ext):
    res = []
    if ext==('cd'):
        for file in os.listdir(fld):
            if file.endswith("._cd"):
                res.append(file)
    elif ext==('snp'):
        snapfld = QFileDialog.getExistingDirectory(fld, 'Select Directory', filter='SNAP (*.snp)')[0]
        print('Hello')
    else:
        QMessageBox.warning()

    return res
