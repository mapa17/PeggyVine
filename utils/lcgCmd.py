'''
Created on Mar 23, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import lcg_util

class lcgCmd(object):

    def __init__(self):
        pass
    
    def cp(src, dest, vo):
        
        print("Trying to copy from [%s] to [%s] with vo [%s]" % ( src, dest, vo ))
        
        result = lcg_util.lcg_cp(src, dest, vo, 1, "", 0, 0)
        print("cp returned %d" % result)
    
    def cr( src, dest, se, vo ):
        result = lcg_util.lcg_cr(src, se, "", dest, vo, "", 1, "", 0, 0, "")
        print("cr returned %d" % result)
        
    cr = staticmethod(cr)
    cp = staticmethod(cp)