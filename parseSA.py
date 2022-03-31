import os
from fnmatch import fnmatch

root = '.\\'
pattern = 'SA_summary.dat'
newSA = 'Col_SA_summary.dat'

fcnt = int(0)
with open(newSA,'w') as outfile:
   for path, subdirs, files in os.walk(root):
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


            # outfile.write("\n")
# print(fcnt)


# fList = glob.glob('SA_summary.dat')
# print(fList)

# csv.register_dialect('skip_space', skipinitialspace=True)
# with open('.\\SA_summary.dat', newline='') as SAfile:
#    reader = csv.reader(SAfile, delimiter=' ', dialect='skip_space')
#    for row in reader:
#       print(row)

# type(file)

# print('Read done')
