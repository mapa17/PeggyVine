'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import os
import sys
import re

from utils.SimpleShell import Shell
from utils.lfcCmd import lfcCmd


class lfcShell (Shell):

    def __init__(self):
        super(lfcShell, self).__init__()
       
        #Add all important cmds
        self.addCmd("put", self._put )
        self.addCmd("get", self._get )
        self.addCmd("info", self._info )
        
        self.addCmd("cd", self._cd )
        self.addCmd("ls", self._ls )
        self.addCmd("LS", self._ls )
        self.addCmd("pwd", self._pwd )
        
        #Override the currentPath 
        self._currentLFCPath = os.environ["LFC_HOME"]
        
        #Store file listeing of current directory, will be updated by _ls and by _cd
        self._currentFileList = self._lfc_getDirListing(self._currentLFCPath)
        
    def _put(self, args):
        raise NotImplementedError("Missing implementation of put")
    
    def _get(self, args):
        raise NotImplementedError("Missing implementation of get")

    def _info(self, args):
        raise NotImplementedError("Missing implementation of info")
    
    def _cd(self, args):
    
        if(len(args) < 2):
            print("Too few arguments! You have to specify a directory to change to!")
            return
    
        if( args[1] == ".." ):
            path = re.match( "(^.*)\/[^\/]*$", self._currentLFCPath ).group(1) #Trim of path after last /
            if path == "" :
                path = "/"
        else:
            path = self._currentLFCPath + '/' + args[1]
            
        if ( lfcCmd.cd(path) == None ):
            print("Error, entering [%s] was not possible!" % path)
        else:
            print("Entering [%s]" % path)
            self._currentLFCPath = path
        pass
    
    def _pwd(self, args):
        print("%s" % self._currentLFCPath)
        
    def _ls(self, args):
        
        if(args[0] == "LS"):
            fullOut = True
        else:
            fullOut = False
            
        if(len(args) > 2):
            fileList = self._lfc_getDirListing( self._currentLFCPath + '/' + args[1] )
        else:
            fileList = lfcCmd.ls( self._currentLFCPath )
                
        self.self_currentFileList = fileList
        
        for i in fileList:
            owner = i["acl"]["owner"]
            if(fullOut):
                guid = i["GUID"]
            else:
                guid = ""
                owner = re.match(".*CN=([\w|-]*)", owner).group(1)
                
            if( i["type"] == "dir" ):
                sys.stdout.write("d")
            elif( i["type"] == "file" ):
                sys.stdout.write("-")
            else:
                sys.stdout.write("?")
            
            print("%s%s%s \t %s \t %s \t %s \t %s" % (i["acl"]["owner_perm"], i["acl"]["group_perm"], i["acl"]["others_perm"], owner, i["acl"]["group"], guid, i["name"]) )        
    
    def _lfc_getDirListing(self, path):
        return lfcCmd.ls( path )
    
               
       