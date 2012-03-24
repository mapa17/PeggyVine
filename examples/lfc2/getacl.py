#!/usr/bin/python

import sys
import traceback
import os

sys.path.append( os.environ["LCG_LOCATION"] )
import lfc2 as lfc

"""
# Using the lfc_getacl to get ACL entries for a file/directory
"""

if len(sys.argv) < 2:
        print "Syntax: %s <LFC_path>" % sys.argv[0]
        sys.exit(-1)

file = sys.argv[1]

try:
        acls_list = lfc.lfc_getacl(file)
except Exception:
        traceback.print_exc()
        sys.exit(1)

print "Found %s entries for %s" % (len(acls_list), file)
for i in acls_list:
        print "User/Group ID: %d" % i.a_id
        print "ACL Type : %d" % i.a_type
        print "Permissions : %d\n" % i.a_perm