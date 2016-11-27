# system modules
from pprint import pprint
import os, sys
import shutil
from optparse import OptionParser

# custom modules
import XML
import misc_io_funcs as MISC_IO
import misc_debug_funcs as MISC_DEBUG

class MHEG_Bmp:
    
    # This data will exist in all
    # BaseClasses (even uninstantiated ones)
    Name = "MHEG_Bmp"
    
      
    # __init__ is a class constructor
    # __****__ is usually a special class method.
    def __init__(self, jsobj, id):
        # These values are created
        # when the class is instantiated.
       
        self.intEnabled = 1
        self.JSONObj = jsobj
        
        self.strName                 = 'bmp'
        self.strInitiallyActive      = 'false'
        self.strOrigBoxSize          = '1 1'
        self.strOrigPosition         = '1 1'        
        self.intID                   = id
        self.strOrigContent          = "(\"/img/nothing.png\")" 
        self.strID                   = "image"       
        
    def Populate(self):
        #print "MHEG_Rect::Populate::Enter"
        #pprint(self.JSONObj)
        
        # fill in the member properties
        self.strName = self.JSONObj.title.data
        self.strInitiallyActive      = 'True'
        self.strOrigBoxSize          = self.getOrigBoxSize()
        self.strOrigPosition         = self.getOrigPosition()
        self.strOrigContent          = self.getOrigContent()           
        
        self.strID                   = self.JSONObj.id
    
    def GetMHEGObjFragment(self):
        
        strmheg = "";
        strmheg = "{ :Bitmap " + self.strName + \
                   "\n\t:InitiallyActive " + self.strInitiallyActive + \
                   "\n\t:OrigContent :ContentRef " + self.strOrigContent + \
                   "\n\t:OrigBoxSize " + self.strOrigBoxSize + \
                   "\n\t:OrigPosition " + self.strOrigPosition + \
                 "\n}";
        
        return strmheg
    
    
    ###################################
    #    HELPER FUNCTIONS             #
    ###################################
   
    def getOrigBoxSize(self):        
        h = int(float(self.JSONObj.height))
        w = int(float(self.JSONObj.width))        
        boxsize = str(w) + " " + str(h)
        return boxsize
    
    def getOrigPosition(self):        
        x = int(float(self.JSONObj.x))
        #y = 576 - int(float(self.JSONObj.y))-int(float(self.JSONObj.height)) 
        y = int(float(self.JSONObj.y))        
        pos = str(x) + " " + str(y)
        return pos
       
    
    def getOrigContent(self):
        
        try:

            full_path  = self.JSONObj.xlink_href                         
            desc = self.JSONObj.desc.data
            
            folder = self.getValueFromDesc(desc, 'folder')
            
            fname = os.path.basename(full_path)
            
            return "(\""+folder+"/"+fname+"\")"
                    
        except:                
            return "'nothing.png'"
    
    
    def getValueFromDesc(self, desc, key):
        s = desc.split(';')        
        for item in s:
            if(key in item):
                key_val = item.split('=')
                return key_val[1]
               
        return ""
    
    def getStyleAttributeValue(self, style, attr):
        attribute_list = style.split(';')
        
        for eachattr in attribute_list:
            key_val_pair = eachattr.split(':')
            if(attr == key_val_pair[0]):
                #s = eachattr.replace(attr+':','')
                s = key_val_pair[1]
                return s
        
        # not found scenario
        return ""
        
    
    def toString(self):
                
        debug = "strName: " + str(self.strName) + '\n' + \
                "intID: " + str(self.intID) + "\n" + \
                "strInitiallyActive: " + str(self.strInitiallyActive) + "\n" + \
                "strOrigBoxSize: " + str(self.strOrigBoxSize) + "\n" + \
                "strOrigPosition: " + str(self.strOrigPosition) + "\n" + \
                "strOrigContent: " + str(self.strOrigContent) + "\n"
        
        return debug;        
    
    