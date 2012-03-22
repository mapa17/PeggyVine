'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os

sys.path.append( os.environ["LCG_LOCATION"] )
import lfc


class lfcCmd(object):

    users = {}
    groups = {}

    def __init__(self):
        pass
    
    def cd(path):
        dirRef = lfc.lfc_opendirg(path,"")
        return dirRef
    
    def ls(path):
        fileList = []
        
        dirRef = lfcCmd.cd(path)
               
        if( dirRef == None):
            return fileList
        
        try:
            
            entry,rpList = lfc.lfc_readdirxr(dirRef,"")
    
            while entry != None :
                 
                element = {} #Create a hash map for every directory element 
                element["name"] = entry.d_name
                element["acl"] = lfcCmd.getacl(path + '/' + element["name"] )
                
                if entry.guid == "":
                    element["type"] = "dir" #Directory
                    element["GUID"] = ""
                else:
                    element["type"] = "file"
                    element["GUID"] = entry.guid
                     
                    if rpList != None: #Iterate the replication list
                        reps = []
                        for i in range(len(rpList) ):
                            reps.append(rpList[i].sfn)
                        element["Replicas"] = reps 
                
                fileList.append(element)

                entry,rpList = lfc.lfc_readdirxr(dirRef,"")
                
        except Exception , e:
            print("Exception [%s] : %s" % ( str(type(e)) , str(e) ) )

        return fileList
    
    def getacl(path):
        #print("Get acl for %s" % path)
        acl = {}
        nentries, acls_list = lfc.lfc_getacl(path, lfc.CA_MAXACLENTRIES)
        #print "nEntries %d" % nentries
        #print "len %d" % len(acls_list)
        for i in acls_list:
            #print "type %d" % i.a_type
            if( i.a_type == 1): #User permissions
                acl["owner_perm"] = lfcCmd._numToPermString( i.a_perm )
                acl["owner"] = lfcCmd._getusrbyuid(i.a_id)
            elif( i.a_type == 3 ) : #Group permissions
                acl["group_perm"] = lfcCmd._numToPermString( i.a_perm )
                acl["group"] = lfcCmd._getgrpbygid(i.a_id)
            elif( i.a_type == 6 ) : #others permissions
                acl["others_perm"] = lfcCmd._numToPermString( i.a_perm )
        
        return acl

    def _numToPermString(perm):
        t = ""
        #t +=  'r' if( perm & 4) else '-'
        #t +=  'w' if( perm & 2) else '-'
        #t +=  'x' if( perm & 1) else '-'
        t += ( '-', 'r')[ (perm & 4) > 0 ]
        t += ( '-', 'w')[ (perm & 2) > 0 ]
        t += ( '-', 'x')[ (perm & 1) > 0 ]
        return t  
            

    def _getusrbyuid(uid):
        if (lfcCmd.users.has_key(uid)):
            return lfcCmd.users[uid] 
        else:
            name = " "*100
            ret = lfc.lfc_getusrbyuid(uid, name)
            if( ret == 0):
                lfcCmd.users[uid] = name.strip()
                return lfcCmd.users[uid]
            else:
                return "[INVALID UID]"
            
    def _getgrpbygid(gid):
        if (lfcCmd.groups.has_key(gid)):
            return lfcCmd.groups[gid] 
        else:
            name = " "*100
            ret = lfc.lfc_getgrpbygid(gid, name)
            if( ret == 0):
                lfcCmd.groups[gid] = name.strip()
                return lfcCmd.groups[gid]
            else:
                return "[INVALID GID]"
            
            
    cd = staticmethod(cd)
    ls=staticmethod(ls)
    getacl = staticmethod(getacl)
    _numToPermString = staticmethod(_numToPermString)
    _getusrbyuid = staticmethod(_getusrbyuid)
    _getgrpbygid = staticmethod(_getgrpbygid)