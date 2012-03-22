'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os

sys.path.append( os.environ["LCG_LOCATION"] )
import lfc


class lfcCmd(object):

    def __init__(self):
        pass
    
    def ls(path):
        fileList = []
        
        dirRef = lfc.lfc_opendirg(path,"")
        
        try:
            
            entry,rpList = lfc.lfc_readdirxr(dirRef,"")
    
            while entry != None :
                 
                element = {} #Create a hash map for every directory element 
                element["name"] = entry.d_name
                if entry.guid == "":
                    element["type"] = "dir" #Directory
                else:
                    element["type"] = "file"
                    element["GUID"] = entry.guid
                     
                    if rpList != None: #Iterate the replication list
                        reps = []
                        for i in range(len(list) ):
                            reps.append(list[i].sfn)
                        element["Replicas"] = reps 
                
                fileList.append(element)

                entry,rpList = lfc.lfc_readdirxr(dir,"")
                
        except Exception , e:
            pass

        return fileList
    
    def getacl(self, path):
#        result = []
#        nentries, acls_list = lfc.lfc_getacl(path, lfc.CA_MAXACLENTRIES)
#        #print "nEntries %d" % nentries
#        #print "len %d" % len(acls_list)
#        for i in acls_list:
#                print "type %d" % i.a_type
#                if( i.a_type == 1): #User permissions
#                    
#                    
#                buffer = " "
#                for j in range(0,100):
#                  buffer=buffer + " "   
#                if( i.a_type == 1) :
#                        ret = lfc.lfc_getusrbyuid(i.a_id, buffer)
#                else :
#                        ret = lfc.lfc_getgrpbygid(i.a_id, buffer)
#                print "id %d %d %s" % (i.a_id, ret,  buffer) 
#                print "perm %d" % i.a_perm
        pass

    ls=staticmethod(ls) 