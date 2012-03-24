'''
Created on Mar 20, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os
import re
import subprocess

class Shell(object):

    def __init__(self):
        self._cmds = {} #A has holding the cmd as string and the function to call
        
        self.addCmd("q", self._quit )
        self.addCmd("quit", self._quit )
        self.addCmd("exit", self._quit )
 
        self.addCmd("export", self._export )
        self.addCmd("lls", self._lls )
        self.addCmd("x" , self._x)
  
        self._quitFlag = False

        self._env = {}
        self._setEnv("PWD", os.getcwd() )
        
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
                    self._cmds[uinput[0]]( uinput ) #Call the function with the input as argument
                except Exception, e:
                    print("<Error!> %s" % str(e) )
            else :
                print("Cmd [%s] not found!" % uinput[0] )

        print("Exiting shell ...")
   
    def _setEnv(self, key, value):
        self._env[key] = value
    
    def _export(self, args):
        if( len(args) > 2):
            self._setEnv(args[1], args[2] )

        print("Environment")
        for k,v in self._env.iteritems():
            print("%s = %s" % (k , v) )
            
    
    def _x(self, args):
        args.pop(0)
        (rV, output , err) = self.runCmd(args)
        if( rV == 0):
            for l in output : print l
        else:
            for l in err : print l
     
    def _lls(self, args):
        args.pop(0)
        args = ["ls"] + args
        #print("Calling with %s" % c)
        (rV, output , err) = self.runCmd(args)
        if( rV == 0):
            for l in output : print l
        else:
            for l in err : print l
     
    def addCmd(self, cmd, function):
        self._cmds[cmd] = function
        pass

    def runCmd(self, cmds):
        #print("Calling for cmd [%s]" % cmds)
        p = subprocess.Popen(cmds, bufsize=100, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (outp, err) = p.communicate()
        output = outp.split('\n')
        #print("Executed cmd [%s], got [%d , %s , %s ]" % (cmds, p.returncode, output, err) )
        return (p.returncode, output, err)
    
    def _quit(self, args):
        #print("Quit was called with arguments %s" % args)
        self._quitFlag = True

