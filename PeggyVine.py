'''
Created on Mar 20, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os

if os.environ.has_key( "LCG_LOCATION" ) == False :
    print("Error %s environment variable not set! e.g: export LCG_LOCATION = \"/opt/lcg\"" % "LCG_LOCATION")
    sys.exit(-1)

if os.environ.has_key( "LFC_HOME" ) == False :
    print("Error %s environment variable not set! e.g: export LFC_HOME = \"/grid/tut.vo.ibergrid.eu\"" % "LFC_HOME")
    sys.exit(-1)

if os.environ.has_key( "LCG_GFAL_VO" ) == False :
    print("Error %s environment variable not set! e.g: export LCG_GFAL_VO = \"tut.vo.ibergrid.eu\"" % "LCG_GFAL_VO")
    sys.exit(-1)
    
    
    
    


from utils.lfcShell import lfcShell

if __name__ == '__main__':
    
    s = lfcShell()
    s.run()
    pass