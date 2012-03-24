'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import stat
import os

sys.path.append( os.environ["LCG_LOCATION"] + "/lib64/python2.4/site-packages/" )
import lfc2 as lfc


class lfcCmd(object):

    users = {}
    groups = {}

    def __init__(self):
        pass
    
    def cr(self, srcFile, destFile):
        pass
    
    def cd(path):
        dirRef = lfc.lfc_opendir(path)
        return dirRef
    
    def ls(path):
        fileList = []
        
        dirRef = lfcCmd.cd(path)
               
        if( dirRef == None):
            return fileList
        
        try:
            
            entry = lfc.lfc_readdirxr(dirRef)
    
            while entry != None :
                 
                element = {} #Create a hash map for every directory element 
                element["name"] = entry.d_name

                element["acl"] = lfcCmd.getacl(path + '/' + element["name"] )
                
                if( stat.S_ISDIR(entry.filemode) == True ):
                    element["type"] = "dir" #Directory
                    element["GUID"] = ""
                else:
                    element["type"] = "file"
                    element["GUID"] = entry.guid
                     
                    reps = []
                    for i in range( entry.nbreplicas ):
                        reps.append(entry.rep[i].sfn)
                    element["Replicas"] = reps 
                
                fileList.append(element)

                entry = lfc.lfc_readdirxr(dirRef)
                
        except Exception , e:
            print("Exception [%s] : %s" % ( str(type(e)) , str(e) ) )

        return fileList
    
    def getacl(path):
        #print("Get acl for %s" % path)
        acl = {}
        acls_list = lfc.lfc_getacl(path)
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
            name = lfc.lfc_getusrbyuid(uid)
            if( name != None ):
                #print( "Resolving uid %d -> %s" % (uid, name) )
                lfcCmd.users[uid] = name.strip()
                return lfcCmd.users[uid]
            else:
                return "[INVALID UID]"
            
    def _getgrpbygid(gid):
        if (lfcCmd.groups.has_key(gid)):
            return lfcCmd.groups[gid] 
        else:
            name = lfc.lfc_getgrpbygid(gid)
            if( name != None ):
                #print( "Resolving gid %d -> %s" % (gid, name) )
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