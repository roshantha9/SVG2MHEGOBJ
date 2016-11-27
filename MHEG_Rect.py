# system modules
from pprint import pprint
import os, sys
import shutil
from optparse import OptionParser

# custom modules
import XML
import misc_io_funcs as MISC_IO
import misc_debug_funcs as MISC_DEBUG

class MHEG_Rect:
    
    # This data will exist in all
    # BaseClasses (even uninstantiated ones)
    Name = "MHEG_Rect"
    
      
    # __init__ is a class constructor
    # __****__ is usually a special class method.
    def __init__(self, jsobj, id):
        # These values are created
        # when the class is instantiated.
       
        self.intEnabled = 1
        self.JSONObj = jsobj
        
        self.strName                 = 'rct'
        self.strInitiallyActive      = 'false'
        self.strOrigBoxSize          = '1 1'
        self.strOrigPosition         = '1 1'
        self.strOrigLineWidth        = '0'
        self.strOrigRefFillColour    = '=FF=FF=FF=00'
        self.intID                   = id
        self.strID                   = 'rect'
        
        
    def Populate(self):
        #print "MHEG_Rect::Populate::Enter"
        #pprint(self.JSONObj)
        
        # fill in the member properties
        self.strName = self.JSONObj.title.data
        self.strInitiallyActive      = 'True'
        self.strOrigBoxSize          = self.getOrigBoxSize()
        self.strOrigPosition         = self.getOrigPosition()
        self.strOrigLineWidth        = self.getLineWidth();
        self.strOrigRefFillColour    = self.getFillColour();
        
        self.strID                   = self.JSONObj.id
        
   
    
    def GetMHEGObjFragment(self):
        
        strmheg = "";
        
        strmheg = "{ :Rectangle " + self.strName + \
                  "\n\t:InitiallyActive " + self.strInitiallyActive + \
                  "\n\t:OrigBoxSize " + self.strOrigBoxSize + \
                  "\n\t:OrigPosition " + self.strOrigPosition + \
                  "\n\t:OrigLineWidth " + self.strOrigLineWidth + \
                  "\n\t:OrigRefFillColour " + self.strOrigRefFillColour + \
                  "\n}";
        
        return strmheg;
    
    
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
    
    
    def getLineWidth(self):        
        style = self.JSONObj.style              
        stroke_width = self.getStyleAttributeValue(style, 'stroke-width').replace('px','')        
        return stroke_width
    
    def getFillColour(self):        
        style = self.JSONObj.style              
        s = self.getStyleAttributeValue(style, 'fill').replace('px','').replace('#','').upper()
        
        fill = "'="+s[0]+s[1]+"="+s[2]+s[3]+"="+s[4]+s[5]+"="+self.getOpacityValue(style)+"'"
        
        return fill    
    
    
    def getOpacityValue(self, style):        
        #print "getOpacityValue:Enter"              
        s = self.getStyleAttributeValue(style, 'opacity').replace('px','').replace('#','').upper()   
        
        if(s == ""):
            s = 1
          
        opacity_hex = hex(int(255-(float(s) * 255)))[2:]
        if(opacity_hex == '0'):
            opacity_hex = '00'
            
        return opacity_hex.upper()
    
    
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
            "strOrigLineWidth: " + str(self.strOrigLineWidth) + "\n" + \
            "strOrigRefFillColour: " + str(self.strOrigRefFillColour) + "\n"; 
             
        
        return debug;        
    
    