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


class gridShell (Shell):

    def __init__(self):
        super(gridShell, self).__init__()
       
        #Add all important cmds
        self.addCmd("put", [ self._put , "Uploads local file to LFC and SE specified" , "... SRC_FILE LFC_DIR SE_INDEX\nUploads SRC_FILE to LFC_DIR and registers it to the SE specified by SE_INDEX.\nA index of SE can be acquired by running the se command."])
        self.addCmd("putlib", [ self._putlib , "Uploads local file to LFC and SE specified" , "... SRC_FILE LFC_DIR SE_INDEX\nUploads SRC_FILE to LFC_DIR and registers it to the SE specified by SE_INDEX.\nA index of SE can be acquired by running the se command."])
        self.addCmd("get", [ self._get , "Downloads a file from LFC" , "... LFC_SRC LOCAL_DEST\nDownloads LFS_SRC from LFC to local disk specified by LOCAL_DEST." ])
        self.addCmd("info", [ self._info , "???"] )
        self.addCmd("se", [ self._se , "Prints list of known SE for current VO" , "\nPrints a list of known SE and their index."])
        
        self.addCmd("cd", [ self._cd , "Changes current LFC directory" , "... LFC_DIR\nChanges to LFC_DIR" ])
        self.addCmd("ls", [ self._ls , "Lists content of current LFC directory" , " ... [DIR|FILE]\nGenerates a file listening of current LFC directory or PATH specified." ])
        self.addCmd("ls1", [ self._ls1 , "Lists content of current LFC directory" , " ... [DIR|FILE]\nGenerates a file listening of current LFC directory or PATH specified." ])
        self.addCmd("LS", [ self._ls , "Verbose listening of current LFC directory" , " ... [DIR|FILE]\nGenerates a verbose! file listening of current LFC directory or PATH specified."] )
        self.addCmd("pwd", [ self._pwd , "Prints path of current LFC directory" , "\nSimply print current LFC directory."] )
        self.addCmd("setSe", [ self._setSe , "Set default SE by index" , "... SE_INDEX"] )  
        
        #Override the currentPath 
        self._setEnv( "LFCPWD" , os.environ["LFC_HOME"])
        self._setEnv( "VO" , os.environ["LCG_GFAL_VO"])
        self._setEnv( "DEFAULT_SE", "")
        #Store file listeing of current directory, will be updated by _ls and by _cd
        self._currentFileList = [] #self._lfc_getDirListing( self._env["LFCPWD"] )
        
        self._seList = []
        self._getSeList()
        self._setSe(["setSe", 0])
        self._se([])
        print("Have set default SE to [%s], use setSe to change this\n" % self._seList[0])
        
        
    def _se(self, args):
        
        if( len( self._seList ) == 0 ):
            self._getSeList()
       
        print("Replica List for VO %s" % self._env["VO"])
        for idx, val in enumerate(self._seList) :
            print("%d) %s" % (idx, val) )
   
    def _setSe(self, args):
        seidx = int(args[1])
        if( (seidx == None) or (seidx < 0)  or (seidx > len(self._seList)) ):
            print("Illegal se index! Valid se index are:\n%s" % self._seList )
        else:
            print("Setting default se to [%s]" % self._seList[seidx])
            self._setEnv( "DEFAULT_SE", self._seList[seidx])

    
    def _getSeList(self):
        
        (retValue, output) = self.runCmdArray( [ "lcg-infosites" , "se" , "--vo", self._env["VO"] ] )
        #print("Found se list [%s]" % output )
        self._seList = []
        for l in output:
            t = re.search("\w*SRM\s*(\S*)", l)
            if( t == None):
                continue
            t = t.group(1)
            if(t != ""):
                self._seList.append( t )
        
    def _put(self, args):
        self._putReal(args, cmdVersion = True)
    
    def _putlib(self, args):
        self._putReal(args, cmdVersion = False)
    
    def _putReal(self, args, cmdVersion = True):
        
        if(len(args) == 2):
            args.append(args[1]) #Save file on catalog with the same name as the source file
        
        if(len(args) == 3):
            se = self._env["DEFAULT_SE"]
            if(se == ""):
                print("You have to specify a default SE! (using setSe <Index>")
                return
        
        if(len(args) == 4):
            seidx = int(args[3])
            if( (seidx == None) or (seidx < 0)  or (seidx > len(self._seList)) ):
                print("Illegal se index! Valid se index are:\n%s" % self._seList )
                return
            
            se = self._seList[seidx] 
  
        #check if path is absolute or relative
        if(args[1][0] == '/'):
            src = "file:" + args[1]
        else:    
            src = "file:" + self._env["LPWD"] + "/" + args[1]

        #check if path is absolute or relative
        if(args[2][0] == '/'):
            dest = args[2] #Absolute path
        else:    
            dest = self._env["LFCPWD"] + "/" + args[2]
        
        if(cmdVersion == True):
            exeCmd = lcgCmd.crStr( src, dest, se, self._env["VO"] )
            print("Will execute cmd [%s]\n" % exeCmd)
            (status, output) = self.runCmd(exeCmd)
            if(status != 0):
                print("Error: [%s]" % output)
            else:
                print("Success!")
        else:
            (returncode, actual_guid, errmsg) = lcgCmd.cr( src, dest, se, self._env["VO"] )
            if(returncode != 0):
                print("Error! [%s]\n" % errmsg)
            else:
                print("Copied file, registered with guid %s" % actual_guid)
            
    
        
    def _get(self, args):
        self._getReal(args, cmdVersion = True)
    
    def _getlib(self, args):
        self._getReal(args, cmdVersion = False)
    
    
    #e.g. lcg-cp --vo your_vo lfn:/grid/your_vo/your_username/text_file.txt file://$PWD/text_file.txt
    def _getReal(self, args, cmdVersion = True):
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
        if(cmdVersion == True):
            exeCmd = lcgCmd.cpStr( src, dest, self._env["VO"] )
            print("Will execute cmd [%s]\n" % exeCmd)
            (status, output) = self.runCmd(exeCmd)
            if(status != 0):
                print("Error: [%s]" % output)
            else:
                print("Sucess: [%s]" % output)
        else:
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
            
            path = os.path.realpath(path) #Remove ../../ elements and make a compact path out of it
            
        if ( lfcCmd.cd(path) == None ):
            print("Error, entering [%s] was not possible!" % path)
        else:
            print("Entering [%s]" % path)
            self._env["LFCPWD"] = path
        pass
    
    def _pwd(self, args):
        print("%s" % self._env["LFCPWD"])
    
    def _ls1(self, args):
        self._ls(args, version = 1)
    
    def _ls(self, args, version = 2):
        
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
                
        fileList = self._lfc_getDirListing( path , version )
        
        self._currentFileList = fileList
        
        for i in fileList:
            
            if( i["type"] == "dir" ):
                fileType = "d"
            elif( i["type"] == "file" ):
                fileType = "-"
            else:
                fileType = "?"
            
            owner = i["acl"]["owner"]
            
            if(fullOut):
                guid = i["GUID"]
                outputformat = "\n%s%s%s%s \t %-50s \t %15s \t %20s \t %s"
                print( outputformat % (fileType, i["acl"]["owner_perm"], i["acl"]["group_perm"], i["acl"]["others_perm"], owner, i["acl"]["group"], guid, i["name"]) )
                
                if( i["type"] == "file" ):                
                    reps = i["Replicas"]
                    if(len(reps) == 0):
                        print("\t\t<No replicas>")
                    else:
                        for j in range(len(reps)) :
                            print( "[%d] %-10s" % (j, reps[j]) )
            else:
                guid = ""
                owner = re.search(".*CN=([\w|-]*)", owner).group(1)
                outputformat = "%s%s%s%s \t %-20s \t %15s \t %20s \t %s"                
                print( outputformat % (fileType, i["acl"]["owner_perm"], i["acl"]["group_perm"], i["acl"]["others_perm"], owner, i["acl"]["group"], guid, i["name"]) )        
    
    def _lfc_getDirListing(self, path, version=2):
        return lfcCmd.ls( path , version)
