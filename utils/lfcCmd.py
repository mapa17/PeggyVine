'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import stat
import os

sys.path.append( os.environ["LCG_LOCATION"] + "/lib64/python2.4/site-packages/" )
#import lfc2 as lfc
import lfc2 as lfc
import lfc as lfc1

class lfcCmd(object):

    users = {}
    groups = {}

    def __init__(self):
        pass
    
    def cr(self, srcFile, destFile):
        pass
    
    def cd(path, version = 2):
        if(version == 1):
            #import lfc
            return lfc1.lfc_opendirg(path,"")
        else:
            return lfc.lfc_opendir(path)
    
    def _ls1(path):
        #import lfc
        fileList = []
        
        dirRef = lfcCmd.cd(path, version=1)
               
        if( dirRef == None):
            err_num = lfc.cvar.serrno
            err_string = lfc.sstrerror(err_num)
            print("Could not get a dir Reference! Error [%s]" % err_string)
            return fileList
        
        try:
            
            while 1 :
                readpT = lfc1.lfc_readdirxr(dirRef,"")
                
                if(readpT == None):
                    break;
                entry, list = readpT
                 
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
                    for i in range( len(list) ):
                        reps.append(list[i].sfn)
                    element["Replicas"] = reps 
                
                fileList.append(element)

                
        except Exception , e:
            print("Exception [%s] : %s" % ( str(type(e)) , str(e) ) )

        lfc1.lfc_closedir(dirRef)
        return fileList
    
    def ls(path, version = 2):
        if(version == 1):
            return lfcCmd._ls1(path)
        else:
            return lfcCmd._ls2(path)
        
    def _ls2(path):
        fileList = []
        
        dirRef = lfcCmd.cd(path, version=2)
               
        if( dirRef == None):
            print("Could not get a dir Reference!")
            return fileList
        
        try:
            
            entry = lfc.lfc_readdirxr(dirRef)
    
            while entry != None :
                 
                element = {} #Create a hash map for every directory element 
                element["name"] = entry.d_name

                print("Get acl...\n")
                element["acl"] = lfcCmd.getacl(path + '/' + element["name"] )
                
                if( stat.S_ISDIR(entry.filemode) == True ):
                    element["type"] = "dir" #Directory
                    element["GUID"] = ""
                else:
                    element["type"] = "file"
                    element["GUID"] = entry.guid
                     
                    print("Get Replicate list [%d] elements\n"%entry.nbreplicas)
                    reps = []
                    for i in range( entry.nbreplicas ):
                        reps.append(entry.rep[i].sfn)
                    element["Replicas"] = reps 
                
                fileList.append(element)
                
                print("Next ...\n")
                entry = lfc.lfc_readdirxr(dirRef)
                
        except Exception , e:
            print("Exception [%s] : %s" % ( str(type(e)) , str(e) ) )

        lfc.lfc_closedir(dirRef)
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
            
      
    ls=staticmethod(ls)      
    _ls1=staticmethod(_ls1)
    cd = staticmethod(cd)
    _ls2=staticmethod(_ls2)
    getacl = staticmethod(getacl)
    _numToPermString = staticmethod(_numToPermString)
    _getusrbyuid = staticmethod(_getusrbyuid)
    _getgrpbygid = staticmethod(_getgrpbygid)