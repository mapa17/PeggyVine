#!/usr/bin/python

import sys
import traceback
#import lfc2 as lfc
sys.path.append("/opt/lcg")
import lfc as lfc

"""
# stat an existing entry in the LFC and print the GUID
"""

if len(sys.argv) < 2:
    print "Syntax: %s <LFC_directory>" % sys.argv[0]
    sys.exit(-1)

name = sys.argv[1]

try:
    stat = lfc.lfc_statg(name,"")

except Exception:
    traceback.print_exc()
    sys.exit(1)

guid = stat.guid
print "The GUID for " + name + " is " + guid