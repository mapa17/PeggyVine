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
from utils import SimpleShell


class lfcShell (Shell):

    def __init__(self):
        super(lfcShell, self).__init__()
       
        #Add all important cmds
        self.addCmd("put", [ self._put , "Uploads local file to LFC and SE specified" , "... SRC_FILE LFC_DIR SE_INDEX\nUploads SRC_FILE to LFC_DIR and registers it to the SE specified by SE_INDEX.\nA index of SE can be acquired by running the se command."])
        self.addCmd("get", [ self._get , "Downloads a file from LFC" , "... LFC_SRC LOCAL_DEST\nDownloads LFS_SRC from LFC to local disk specified by LOCAL_DEST." ])
        self.addCmd("info", [ self._info , "???"] )
        self.addCmd("se", [ self._se , "Prints list of known SE for current VO" , "\nPrints a list of known SE and their index."])
        
        self.addCmd("cd", [ self._cd , "Changes current LFC directory" , "... LFC_DIR\nChanges to LFC_DIR" ])
        self.addCmd("ls", [ self._ls , "Lists content of current LFC directory" , " ... [DIR|FILE]\nGenerates a file listening of current LFC directory or PATH specified." ])
        self.addCmd("LS", [ self._ls , "Verbose listening of current LFC directory" , " ... [DIR|FILE]\nGenerates a verbose! file listening of current LFC directory or PATH specified."] )
        self.addCmd("pwd", [ self._pwd , "Prints path of current LFC directory" , "\nSimply print current LFC directory."] )
        
         
        
        #Override the currentPath 
        self._setEnv( "LFCPWD" , os.environ["LFC_HOME"])
        self._setEnv( "VO" , os.environ["LCG_GFAL_VO"])
        
        #Store file listeing of current directory, will be updated by _ls and by _cd
        self._currentFileList = [] #self._lfc_getDirListing( self._env["LFCPWD"] )
        
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
            print("Too few arguments! Usage:\n%s %s" % ( args[0] , self._env[args[0]][self.HELP_IDX]) )
            return
  
  #lcg-cr --vo your_vo -d srm://srm.grid.sara.nl:8443/pnfs/grid.sara.nl/data/your_vo/your_dir/text_file.txt \
  # -l lfn:/grid/your_vo/your_username/text_file.txt "file://$PWD/text_file.txt"
        
        #check if path is absolute or relative
        if(args[1][0] == '/'):
            src = "file:" + args[1]
        else:    
            src = "file:" + self._env["LPWD"] + "/" + args[1]

        #check if path is absolute or relative
        if(args[1][0] == '/'):
            dest = "lfn:" + args[2]
        else:    
            dest = "lfn:/" + self._env["LFCPWD"] + "/" + args[2]
        
        seidx = int(args[3])
        if( (seidx == None) or (seidx < 0)  or (seidx > len(self._seList)) ):
            print("Illegal se index! Valid se index are:\n%s" % self._seList )
            return
        
        se = self._seList[seidx] 
            
        lcgCmd.cr( src, dest, se, self._env["VO"] ) 
        
        
    def _get(self, args):
        if(len(args) < 2):
            print("Too few arguments! Usage:\n%s %s" % ( args[0] , self._env[args[0]][self.HELP_IDX]) )
            return
        
        #check if path is absolute or relative
        if(args[1][0] == '/'):
            src = "lfn:" + args[1]
        else:    
            src = "lfn:" + self._env["LFCPWD"] + "/" + args[1]
        
        if( len(args) == 2):
            dest = "file:" + self._env["LPWD"] + "/" + args[1].split("/").pop() #Take same local filename as remote one            
        else:
            #check if path is absolute or relative
            if(args[2][0] == '/'):
                dest = args[2]
            else:    
                dest = "file:" + self._env["LPWD"] + "/" + args[2]
            
        lcgCmd.cp( src, dest, self._env["VO"] )

    def _info(self, args):
        raise NotImplementedError("Missing implementation of info")
    
    
    def _cd(self, args):
    
        if(len(args) < 2):
            print("Too few arguments! Usage:\n%s %s" % ( args[0] , self._env[args[0]][self.HELP_IDX]) )
            return
    
        if( args[1] == ".." ):
            path = re.search( "(^.*)\/[^\/]*$", self._env["LFCPWD"] ).group(1) #Trim of path after last /
            if path == "" :
                path = "/"
        else:
            #check if path is absolute or relative
            if(args[1][0] == '/'):
                path = args[1]
            else:    
                path = self._env["LFCPWD"] + '/' + args[1]
            
        if ( lfcCmd.cd(path) == None ):
            print("Error, entering [%s] was not possible!" % path)
        else:
            print("Entering [%s]" % path)
            self._env["LFCPWD"] = path
        pass
    
    def _pwd(self, args):
        print("%s" % self._env["LFCPWD"])
        
    def _ls(self, args):
        
        if(args[0] == "LS"):
            fullOut = True
        else:
            fullOut = False
            
        if(len(args) > 2):
            #check if path is absolute or relative
            if(args[1][0] == '/'):
                path = args[1]
            else:    
                path = self._env["LFCPWD"] + '/' + args[1]
        else:
            path = self._env["LFCPWD"]
                
        fileList = self._lfc_getDirListing( path )
        
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
    
               
       