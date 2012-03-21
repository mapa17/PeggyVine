'''
Created on Mar 20, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import re
import subprocess

class Shell(object):

    def __init__(self):
        self._cmds = {} #A has holding the cmd as string and the function to call
        
        self.addCmd("q", self._quit )
        self.addCmd("quit", self._quit )
        self.addCmd("exit", self._quit )
        
        self._quitFlag = False
        
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
    
    def addCmd(self, cmd, function):
        self._cmds[cmd] = function
        pass

    def runCmd(self, cmds):
        #print("Calling for cmd [%s]" % cmds)
        p = subprocess.Popen(cmds, bufsize=100, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (outp, err) = p.communicate()
        output = outp.split('\n')
        #print("Executed cmd [%s], got [%s]" % (cmds, output) )
        return (p.returncode, output, err)
    
    def _quit(self, args):
        #print("Quit was called with arguments %s" % args)
        self._quitFlag = True

