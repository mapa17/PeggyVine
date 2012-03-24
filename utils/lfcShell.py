'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import os
import sys
import re

from utils.SimpleShell import Shell
from utils.lfcCmd import lfcCmd
from utils.lcgCmd import lcgCmd


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
        
        self.addCmd("se", self._se ) 
        
        #Override the currentPath 
        self._setEnv( "LFCPath" , os.environ["LFC_HOME"])
        self._setEnv( "VO" , os.environ["LCG_GFAL_VO"])
        
        #Store file listeing of current directory, will be updated by _ls and by _cd
        self._currentFileList = [] #self._lfc_getDirListing( self._env["LFCPath"] )
        
        self._seList = []
        
    def _se(self, args):
        
        if( len( self._seList ) == 0 ):
            self._getSeList()
       
        print("Replica List for VO %s" % self._env["VO"])
        for idx, val in enumerate(self._seList) :
            print("%d) %s" % (idx, val) )
    
    def _getSeList(self):
        
        (retValue, output, err) = self.runCmd( [ "lcg-infosites" , "se" , "--vo", self._env["VO"] ] )
        print("Found se list [%s]" % output )
        self._seList = []
        for l in output:
            t = re.search("\w*SRM\s*(\S*)", l)
            if( t == None):
                continue
            t = t.group(1)
            if(t != ""):
                self._seList.append( t )
        
    def _put(self, args):
        if(len(args) < 4):
            print("Too few arguments! [%s] [src_file] [lfn direction] [index of se]" % ( args[0] ))
            return
  
  #lcg-cr --vo your_vo -d srm://srm.grid.sara.nl:8443/pnfs/grid.sara.nl/data/your_vo/your_dir/text_file.txt \
  # -l lfn:/grid/your_vo/your_username/text_file.txt "file://$PWD/text_file.txt"
        
        dest = "lfn:/" + self._env["LFCPath"] + "/" + args[2]
        
        src = "file://" + self._env["PWD"] + "/" + args[1]
        
        seidx = int(args[3])
        if( (seidx == None) or (seidx < 0)  or (seidx > len(self._seList)) ):
            print("Illegal se index!")
            return
        
        se = self._seList[seidx] 
            
        lcgCmd.cr( src, dest, se, self._env["VO"] ) 
        
        
    def _get(self, args):
        if(len(args) < 2):
            print("Too few arguments! [%s] [src_file] <dest_file]>" % ( args[0] ))
            return
        
        src = "lfn:/" + self._env["LFCPath"] + "/" + args[1]
        
        if( len(args) == 2):
            dest = "file://" + self._env["PWD"] + "/" + args[1]            
        else:
            dest = "file://" + self._env["PWD"] + "/" + args[2]
            
        lcgCmd.cp( src, dest, self._env["VO"] )

    def _info(self, args):
        raise NotImplementedError("Missing implementation of info")
    
    
    def _cd(self, args):
    
        if(len(args) < 2):
            print("Too few arguments! You have to specify a directory to change to!")
            return
    
        if( args[1] == ".." ):
            path = re.search( "(^.*)\/[^\/]*$", self._env["LFCPath"] ).group(1) #Trim of path after last /
            if path == "" :
                path = "/"
        else:
            path = self._env["LFCPath"] + '/' + args[1]
            
        if ( lfcCmd.cd(path) == None ):
            print("Error, entering [%s] was not possible!" % path)
        else:
            print("Entering [%s]" % path)
            self._env["LFCPath"] = path
        pass
    
    def _pwd(self, args):
        print("%s" % self._env["LFCPath"])
        
    def _ls(self, args):
        
        if(args[0] == "LS"):
            fullOut = True
        else:
            fullOut = False
            
        if(len(args) > 2):
            fileList = self._lfc_getDirListing( self._env["LFCPath"] + '/' + args[1] )
        else:
            fileList = lfcCmd.ls( self._env["LFCPath"] )
                
        self._currentFileList = fileList
        
        for i in fileList:
            
            owner = i["acl"]["owner"]
            if(fullOut):
                guid = i["GUID"]
                outputformat = "%s%s%s \t %-50s \t %15s \t %20s \t %s"
            else:
                guid = ""
                owner = re.search(".*CN=([\w|-]*)", owner).group(1)
                outputformat = "%s%s%s \t %-20s \t %15s \t %20s \t %s"
                
            if( i["type"] == "dir" ):
                sys.stdout.write("d")
            elif( i["type"] == "file" ):
                sys.stdout.write("-")
            else:
                sys.stdout.write("?")
            
            print( outputformat % (i["acl"]["owner_perm"], i["acl"]["group_perm"], i["acl"]["others_perm"], owner, i["acl"]["group"], guid, i["name"]) )        
    
    def _lfc_getDirListing(self, path):
        return lfcCmd.ls( path )
    
               
       