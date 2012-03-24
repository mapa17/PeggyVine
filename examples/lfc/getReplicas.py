#!/usr/bin/python

"""
# Using the lfc_readdirxr method
"""

import sys
import traceback

#import lfc2 as lfc
#Add path to lcg library to search path in order to find lfc library
sys.path.append("/opt/lcg")
import lfc as lfc


try:
    if len(sys.argv) < 2:
        print "Syntax: %s <LFC_directory>" % sys.argv[0]
        sys.exit(-1)

    name = sys.argv[1]

    dir = lfc.lfc_opendir(name)

    while 1:
        entry = lfc.lfc_readdirxr(dir)
        if entry == None:
            break
        print entry.d_name
        for i in range(entry.nbreplicas):
            print " ==> %s" % entry.rep[i].sfn

    lfc.lfc_closedir(dir)
    
except TypeError, x:
    print " ==> None"
except Exception:
    traceback.print_exc()
    sys.exit(1)
