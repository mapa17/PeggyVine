#!/usr/bin/python

import sys
import traceback

sys.path.append("/opt/lcg")
import lfc

"""
# Using the lfc_getacl to get ACL entries for a file/directory
"""

if len(sys.argv) < 2:
        print "Syntax: %s <LFC_path>" % sys.argv[0]
        sys.exit(-1)

name = sys.argv[1]


dir = lfc.lfc_opendirg(name,"")


entry,list = lfc.lfc_readdirxr(dir,"")
while entry != None : 
        print "---"
        print entry.d_name
        if entry.guid == "":
                print "Dir"
        else:
                print entry.guid
        if list != None:
                for i in range(len(list) ):
                        print list[i].sfn 
        try:
                entry,list = lfc.lfc_readdirxr(dir,"")
        except Exception , e:
                break 

print "End of dir reached!"
