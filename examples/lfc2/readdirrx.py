"""
# Using the lfc_readdirxr to retrieve guid and replicas of an LFC entry 
"""

import sys,stat
import traceback
import os

sys.path.append( os.environ["LCG_LOCATION"] )
import lfc2 as lfc

if len(sys.argv) < 2:
        print "Syntax: %s <LFC_directory>" % sys.argv[0]
        sys.exit(-1)

name = sys.argv[1]

dir = lfc.lfc_opendir(name)
if (dir == None) or (dir == 0):
        print  "Error  while  looking  for  " + name + ": No such a file or directory"
        sys.exit(1)

try:
        while 1:
                entry = lfc.lfc_readdirxr(dir)
                if entry == None:
                        break
                print entry.d_name
                if stat.S_ISDIR(entry.filemode):
                        print " ==> Directory"
                else:
                        print "GUID : %s" % entry.guid
                        for i in range(entry.nbreplicas):
                                print " ==> %s" % entry.rep[i].sfn

        lfc.lfc_closedir(dir)
except TypeError, x:
        print " ==> None"
except Exception:
        traceback.print_exc()
        sys.exit(1)