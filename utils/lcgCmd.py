'''
Created on Mar 23, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

#sys.path.append( os.environ["LCG_LOCATION"] + "/lib64/python2.4/site-packages/" )
import lcg_util

class lcgCmd(object):

    def __init__(self):
        pass
 
    def cp(src, dest, vo):
        
        src_file=src
        dest_file=dest
        vo=vo
        nbstreams=1
        conf_file=''
        insecure=0
        verbose=0
        
        print("Trying to copy from [%s] to [%s] with vo [%s]" % ( src, dest, vo ))
        
        result = lcg_util.lcg_cp(src_file, dest_file, vo, nbstreams, conf_file, insecure, verbose)
        print("cp returned %d" % result)
 
    #(returncode, actual_guid, errmsg)=lcg_util.lcg_cr(src_file, dest_file, guid, lfn, vo, relativepath, nbstreams, conf_file, insecure, verbose)
    #lcg-cr -d ngiesse.i3m.upv.es -l lfn:/grid/tut.vo.ibergrid.eu/pegos/R1 --vo tut.vo.ibergrid.eu README   
    #(returncode, actual_guid, errmsg)=lcg_util.lcg_cr3(src_file, dest_file, guid, lfn, defaulttype, setype, nobdii, vo, relativepath, nbstreams, conf_file, insecure, verbose, timeout, spacetokendesc)
    def cr( src, dest, se, vo ):
        
        src_file=src
        dest_file=se
        guid=''
        lfn=dest
        defaulttype=''
        setype=''
        nobdii=0
        
        relativepath=''
        nbstreams=1
        conf_file=''
        insecure=0
        verbose=1
        timeout=0
        spacetokendesc=''
        
        print("Calling cr with src:[%s] to [%s] on [%s] for vo [%s]"%(src, dest, se, vo))
        
        #(returncode, actual_guid, errmsg)=lcg_util.lcg_cr(src_file, dest_file, guid, lfn, vo, relativepath, nbstreams, conf_file, insecure, verbose)
        (returncode, actual_guid, errmsg)=lcg_util.lcg_cr3(src_file, dest_file, guid, lfn, defaulttype, setype, nobdii, vo, relativepath, nbstreams, conf_file, insecure, verbose, timeout, spacetokendesc)
        return (returncode, actual_guid, errmsg)
        
    def crStr( src, dest, se, vo ):
        s = "lcg-cr -d %s -l lfn:%s --vo %s %s"%(se, dest, vo, src)
        return s
        
        
    crStr = staticmethod(crStr)
    cr = staticmethod(cr)
    cp = staticmethod(cp)