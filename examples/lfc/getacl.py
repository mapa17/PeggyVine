#!/usr/bin/python

import sys
import os

sys.path.append( os.environ["LCG_LOCATION"] )
import lfc

"""
# Using the lfc_getacl and lfc_setacl methods to add a user ACL
"""
if len(sys.argv) < 2:
        print "Syntax: %s <LFC_path>" % sys.argv[0]
        sys.exit(-1)

name = sys.argv[1]

nentries, acls_list = lfc.lfc_getacl(name, lfc.CA_MAXACLENTRIES)
print "nEntries %d" % nentries
print "len %d" % len(acls_list)
for i in acls_list:
        print "type %d" % i.a_type
        buffer = " "
        for j in range(0,100):
          buffer=buffer + " "   
        if( i.a_type == 1) :
                ret = lfc.lfc_getusrbyuid(i.a_id, buffer)
        else :
                ret = lfc.lfc_getgrpbygid(i.a_id, buffer)
        print "id %d %d %s" % (i.a_id, ret,  buffer) 
        print "perm %d" % i.a_perm
