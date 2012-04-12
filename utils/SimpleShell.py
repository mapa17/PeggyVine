'''
Created on Mar 20, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os
import re
import commands

class Shell(object):

    CMD_IDX = 0
    DESC_IDX = 1
    HELP_IDX = 2

    def __init__(self):
        self._cmds = {} #A has holding the cmd as string and the function to call
        
        self.addCmd("q", [ self._quit , "Quit application" , "\nQuit application" ] )
        self.addCmd("quit", [ self._quit , "Quit application" , "\nQuit application" ] )
        self.addCmd("exit", [ self._quit , "Quit application" , "\nQuit application" ] )
 
        self.addCmd("export", [ self._export , "Print and set environment variables" , " ... [ENV_NAME = VALUE]\nIf no ENV_NAME is specified, current environment variables are printed."] )
        self.addCmd("lls", [ self._lls , "Generate local file system listening" , "\nPrint content of local file system directory."])
        self.addCmd("lcd", [ self._lcd , "Change local file system directory" , "... [DIRECTORY]\nChanges local active directory to DIRECTORY"] )
        self.addCmd("lpwd", [ self._lpwd , "Prints local current working directory" , "\nSimply print current local directory."] )
        
        self.addCmd("x" , [ self._x , "Run arbitrary shell command" , "... CMD [ARG0] [ARG1] ... [ARGX]\nExecutes CMD with Arguments specified"] )        
        self.addCmd("help", [ self._help , "Informs about known commands and their usage" , "... [CMD]\nPrints help on CMD" ] )
        
  
        self._quitFlag = False

        self._env = {}
        self._setEnv("LPWD", os.getcwd() )
        
    def run(self):
        
        while( self._quitFlag == False) :
    
            sys.stdout.write(">> ")
            line = sys.stdin.readline()
            #input = re.sub(" +", " ", line) #Reduce multiple spaces to one
            #input = input.strip() #Strip of trailing spaces
            #input = line.split(" ") #Create array out of input
            uinput = re.sub(' +',' ', line).strip().split(" ")
            
            if self._cmds.has_key( uinput[0] ) :
                try:
                    self._cmds[uinput[0]][self.CMD_IDX]( uinput ) #Call the function with the input as argument
                except Exception, e:
                    print("<Error!> %s" % str(e) )
            else :
                print("Cmd [%s] not found!" % uinput[0] )

        print("Exiting shell ...")
   
    def _help(self, args):
        if( len(args) == 1):
            print("Commands:")
            for k,v in self._cmds.iteritems():
                print("%-8s ... %s" % (k , v[self.DESC_IDX]) )
            
        elif( len(args) == 2 ):
            if self._cmds.has_key(args[1] ):
                print( "%-8s %s" % (args[1] , self._cmds[args[1]][self.HELP_IDX] ) )
        else:
            print("Error unknown arguments!\n%-8s %s" % (args[0] , self._cmds[args[0]][self.HELP_IDX] ))
   
    def _setEnv(self, key, value):
        self._env[key] = value
    
    def _export(self, args):
        if( len(args) > 2):
            self._setEnv(args[1], args[2] )

        print("Environment:")
        for k,v in self._env.iteritems():
            print("%s = %s" % (k , v) )
            
    
    def _x(self, args):
        args.pop(0)
        (rV, output) = self.runCmdArray(args)
        for l in output : print l
    
    def _lpwd(self, args):
        print("%s" % self._env["LPWD"])
     
    def _lls(self, args):
        
        if( len(args) == 1):
            path = self._env["LPWD"]
        else:
            #check if path is absolute or relative
            if(args[1][0] == '/'):
                path = args[1]
            else:    
                path = self._env["LPWD"] + args[1]
        
        #print("Calling with %s" % ["ls" , path] )
        (rV, output) = self.runCmd("ls %s" % path)
        for l in output : print l
    
    def _lcd(self, args):
        if( len(args) < 2):
            print("Error! You have to specify target directory! \n Usage: %s TARGET_DIR" % (args[0]) )
            return
        
        #check if path is absolute or relative
        if(args[1][0] == '/'):
            path = args[1]
        else:    
            path = self._env["LPWD"] + args[1]
            
        if( os.path.isdir( path ) == True ):
            self._env["LPWD"] = path
            print("Entering directory [%s] ..." % self._env["LPWD"] )
        else:
            print("Error can't change to [%s]!" % path )
     
    def addCmd(self, cmd, function_array):
        self._cmds[cmd] = function_array
        pass

    def runCmdArray(self, cmdArray):
        cmd = " ".join(cmdArray)
        return self.runCmd(cmd)
        
    def runCmd(self, cmd):
        (status, output) = commands.getstatusoutput(cmd)
        output = output.split('\n')
        return (status, output)
        
        #print("Calling for cmd [%s]" % cmds)
        #p = subprocess.Popen(cmds, bufsize=100, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #(outp, err) = p.communicate()
        #output = outp.split('\n')
        #print("Executed cmd [%s], got [%d , %s , %s ]" % (cmds, p.returncode, output, err) )
        #return (p.returncode, output, err)
    
    def _quit(self, args):
        #print("Quit was called with arguments %s" % args)
        self._quitFlag = True

