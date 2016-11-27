import pprint
import os, sys
import shutil


def read_file(fname, mode):
    
    if(os.path.isfile(fname) and os.path.exists(os.path.dirname(fname))):
        file = open(fname, mode)
        buff = file.read()
        file.close()
        
        return buff
    else:
        error_msg = "ERROR: read_file : file not found :  " + fname
        sys.exit(error_msg)
        
        
# essentially a COPY->PASTE->RENAME
def copy_file(src, dst):
    
    # if dest does not exist create it
    if(os.path.exists(os.path.dirname(dst))==False):
        os.mkdir(os.path.dirname(dst))
    
    if(os.path.isfile(src) and os.path.exists(os.path.dirname(dst))):
        shutil.copyfile(src, dst)
    else:
        print "\nERROR: unable to perform the move, incorrect destination path or source file"
        print "Source - " +  src
        print "Dest. - " + dst
        #sys.exit()

def write_file(fname, data,mode='w'):
    
    if(os.path.exists(os.path.dirname(fname))):       
        file = open(fname, mode)
        file.write(data)
        file.close()
    else: 
        error_msg = "ERROR: write_file : path not found :  " + os.path.dirname(fname)
        sys.exit(error_msg)
        
    
def delete_file(fname):
    if( os.path.isfile(fname) ):
        os.remove(fname) 
        

# essentially a CUT->PASTE->RENAME
def move_file(src, dst):
    
    # if dest does not exist create it
    if(os.path.exists(os.path.dirname(dst))==False):
        os.mkdir(os.path.dirname(dst))
    
    if(os.path.isfile(src) and os.path.exists(os.path.dirname(dst))):
        shutil.move(src, dst)
    else:
        print "\nERROR: unable to perform the move, incorrect destination path or source file"
        print "Source - " +  src
        print "Dest. - " + dst
        #sys.exit()
