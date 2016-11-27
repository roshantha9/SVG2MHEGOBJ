# system modules
from pprint import pprint
import os, sys
import shutil
from optparse import OptionParser

# custom modules
import XML
import misc_io_funcs as MISC_IO
import misc_debug_funcs as MISC_DEBUG

class MHEG_Text:
    
    # This data will exist in all
    # BaseClasses (even uninstantiated ones)
    Name = "MHEG_Text"
    
      
    # __init__ is a class constructor
    # __****__ is usually a special class method.
    def __init__(self, jsobj_rect,jsobj_flowroot, id):
        # These values are created
        # when the class is instantiated.
       
        self.intEnabled = 1
        self.JSONObj_Rect = jsobj_rect
        self.JSONObj_FlowRoot = jsobj_flowroot
        
        self.strName                 = "txt"
        self.strInitiallyActive      = "false"
        self.strOrigBoxSize          = "1 1"
        self.strOrigPosition         = "1 1"
        self.strOrigContent          = "dummy text"         
        self.strFontAttributes       = "plain.16.20.0"
        self.strTextColour           = "=FF=00=00=00"
        self.strBackgroundColour     = "=00=00=00=FF"
        self.strHJustification       = "start"
        self.strVJustification       = "start" 
        self.strTextWrapping         = "True"
        self.intID                   = id
        self.strID                   = "flowRoot"
        
        
    def Populate(self):
        #print "MHEG_Text::Populate::Enter"
        #pprint(self.JSONObj_Rect)
        #pprint(self.JSONObj_FlowRoot)
        
        # fill in the member properties
        self.strName = self.JSONObj_FlowRoot.title.data


#        self.strOrigRefFillColour    = self.getFillColour();


       
        self.strInitiallyActive      = "True"
        self.strOrigBoxSize          = self.getOrigBoxSize()
        self.strOrigPosition         = self.getOrigPosition()
        
        self.strOrigContent          = self.getOrigContent()         
        self.strFontAttributes       = self.getFontAttributes()
        self.strTextColour           = self.getTextColour()
        self.strBackgroundColour     = self.getBackgroundColour()
        self.strHJustification       = self.getHJustification() 
        self.strVJustification       = 'start' 
        self.strTextWrapping         = 'True'            
        
        self.strID                   = self.JSONObj_FlowRoot.id
        
   
    
    def GetMHEGObjFragment(self):
        
        strmheg = "";
        strmheg =   "{ :Text " + self.strName + \
                     "\n\t:InitiallyActive " + self.strInitiallyActive + \
                     "\n\t:OrigContent " + self.strOrigContent + \
                     "\n\t:OrigBoxSize " + self.strOrigBoxSize + \
                     "\n\t:OrigPosition " + self.strOrigPosition + \
                     "\n\t:FontAttributes " + self.strFontAttributes + \
                     "\n\t:TextColour " + self.strTextColour + \
                     "\n\t:BackgroundColour " + self.strBackgroundColour + \
                     "\n\t:HJustification " + self.strHJustification + \
                     "\n\t:VJustification " + self.strVJustification + \
                     "\n\t:TextWrapping " + self.strTextWrapping + \
                     "\n}"       
                     
        return strmheg;
    
    
    ###################################
    #    HELPER FUNCTIONS             #
    ###################################
   
    def getOrigBoxSize(self):        
        h = int(float(self.JSONObj_Rect.height))
        w = int(float(self.JSONObj_Rect.width))        
        boxsize = str(w) + " " + str(h)
        return boxsize
    
    def getOrigPosition(self):        
        x = int(float(self.JSONObj_Rect.x))
        y = int(float(self.JSONObj_Rect.y))        
        pos = str(x) + " " + str(y)
        return pos    
   
    def getBackgroundColour(self):        
        style = self.JSONObj_Rect.style              
        s = self.getStyleAttributeValue(style, 'fill').replace('px','').replace('#','').upper()
        
        fill = "'="+s[0]+s[1]+"="+s[2]+s[3]+"="+s[4]+s[5]+"="+self.getOpacityValue(style)+"'"
        
        return fill    

    def getTextColour(self):        
        #print "getTextColour:Enter"        
        style = self.JSONObj_FlowRoot.style
        s = self.getStyleAttributeValue(style, 'fill').replace('px','').replace('#','').upper()        
        
        fill = "'="+s[0]+s[1]+"="+s[2]+s[3]+"="+s[4]+s[5]+"="+self.getOpacityValue(style)+"'"
        return fill
    
    def getHJustification(self):
        #print "getHJustification:Enter"
        style = self.JSONObj_FlowRoot.style        
        s = self.getStyleAttributeValue(style, 'text-align').replace('px','').replace('#','') 
        
        if (s == ""):
            s = "left"  # default            
            
        if(s == "left"):
            alignment = "start"
        elif (s == "center"):
            alignment = "centre"
        elif (s == "end"):
            alignment = "end"
        else:
            alignment = "start"

        return alignment
    
    
    def getVJustification(self):
        print "getVJustification:Enter"
        style = self.JSONObj_FlowRoot.style        
        s = self.getStyleAttributeValue(style, 'text-align').replace('px','').replace('#','') 
        
        if (s == ""):
            s = "left"  # default            
            
        if(s == "left"):
            alignment = "start"
        elif (s == "center"):
            alignment = "centre"
        elif (s == "end"):
            alignment = "end"
        else:
            alignment = "start"

        return alignment
    
    
    def getFontAttributes(self):        
        #print "getTextColour:Enter"        
        style = self.JSONObj_FlowRoot.style
        s = self.getStyleAttributeValue(style, 'font-size').replace('px','').replace('#','').upper()        
        
        fontattr = "'plain."+s+".20"+".0'"
        
        return fontattr
    
    def getOrigContent(self):
        
        content = ""
        
        for eachpara in self.JSONObj_FlowRoot.flowPara:
            content = content + " " + eachpara.data
        
        content = "'"+content.strip()+"'"
        
        return content
    
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
                
        debug = "\nstrName: " + self.strName + \
                "\nstrInitiallyActive: " + self.strInitiallyActive + \
                "\nstrOrigContent: " + self.strOrigContent + \
                "\nstrOrigBoxSize: " + self.strOrigBoxSize + \
                "\nstrOrigPosition: " + self.strOrigPosition + \
                "\nstrFontAttributes: " + self.strFontAttributes + \
                "\nstrTextColour: " + self.strTextColour + \
                "\nstrBackgroundColour: " + self.strBackgroundColour + \
                "\nstrHJustification: " + self.strHJustification + \
                "\nstrVJustification: " + self.strVJustification + \
                "\nstrTextWrapping: " + self.strTextWrapping + "\n\n"
        
        return debug        
    
    