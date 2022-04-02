import os
from fnmatch import fnmatch

root = '.\\'
pattern = 'SA_summary.dat'
newSA = 'Col_SA_summary.dat'

def mergeSA(fld):
   fcnt = int(0)
   with open(newSA,'w') as outfile:
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

# fcnt = int(0)
# with open(newSA,'w') as outfile:
#    for path, subdirs, files in os.walk(root):
#       for name in files:
#          if fnmatch(name, pattern):
#             fname = os.path.join(path, name)
#             fcnt = fcnt + 1
#             print(fname)
#             with open(fname) as infile:
#                if fcnt < 2:
#                   outfile.write(infile.read())
#                else:
#                   next(infile)
#                   outfile.write(infile.read())