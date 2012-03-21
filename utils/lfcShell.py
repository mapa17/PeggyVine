'''
Created on Mar 21, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

from utils.SimpleShell import Shell

class lfcShell (Shell):

    def __init__(self):
        super(lfcShell, self).__init__()
       
        #Add all important cmds
        self.addCmd("put", self._put )
        self.addCmd("get", self._get )
        self.addCmd("info", self._info )
        
        self.addCmd("ls", self._ls )
        self.addCmd("x" , self._x)
    
    def _put(self, args):
        raise NotImplementedError("Missing implementation of put")
    
    def _get(self, args):
        raise NotImplementedError("Missing implementation of get")

    def _info(self, args):
        raise NotImplementedError("Missing implementation of info")
                  
    def _ls(self, args):
        args.pop(0)
        args = ["ls"] + args
        #print("Calling with %s" % c)
        (rV, output , err) = self.runCmd(args)
        if( rV == 0):
            for l in output : print l
        else:
            for l in err : print l
                
    def _x(self, args):
        args.pop(0)
        (rV, output , err) = self.runCmd(args)
        if( rV == 0):
            for l in output : print l
        else:
            for l in err : print l
        