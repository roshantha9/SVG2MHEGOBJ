# system modules
from pprint import pprint
import os, sys, re
import shutil
from optparse import OptionParser

# custom modules
import XML
import misc_io_funcs as MISC_IO
import misc_debug_funcs as MISC_DEBUG
from MHEG_Rect import MHEG_Rect
from MHEG_Text import MHEG_Text
from MHEG_Bmp import MHEG_Bmp


###################################
#    GLOBALS                      #
###################################

# svg objects list
SVGRectList = []
SVGTextList = []
SVGBmpList  = []

# mheg objects list
MHEGRectList    = []
MHEGTextList    = []
MHEGBmpList     = []

# define counter
intDefineCount = 0

# printout Z-order
Z_order_list_ids = []





###################################
# Extract Object arrays from SVG  #
###################################

# get all rects in the SVG
def SVGExtract_GetRectJSON(SVGPyObj):
    return SVGPyObj.g.rect
    
# get all the flow roots which have xlinks
# returns only the Text specific flow roots    
def SVGExtract_GetTextFlowRootsJSON(SVGPyObj):
    arrayList = []
    for eachflowRoot in SVGPyObj.g.flowRoot:                
        if(eachflowRoot.flowRegion.use != None):
            arrayList.append(eachflowRoot)
            
    return arrayList;


# returns a list of rects referenced by the Text 
# flowroots    
def SVGExtract_GetFlowRoot_Xlink_Rects(SVGPyObj):
    
    # get the specific xlinks related to flowroots
    xlink_arrayList = []
    for eachflowRoot in SVGPyObj.g.flowRoot:                
        if(eachflowRoot.flowRegion.use != None):
            xlink_arrayList.append(eachflowRoot.flowRegion.use.xlink_href.replace('#',''))
         
    #pprint(xlink_arrayList)
    return xlink_arrayList

# returns a list of pure rects, not linked with any
# flowroots
def SVGExtract_GetRects(SVGPyObj):
    xlink_rects_array = SVGExtract_GetFlowRoot_Xlink_Rects(SVGPyObj)
    
    arrayRects = []
    for eachRect in SVGPyObj.g.rect:
        if not(any(eachRect.id in s for s in xlink_rects_array)):
            arrayRects.append(eachRect)
    
    return arrayRects  


# returns a list of pure rects, not linked with any
# flowroots
def SVGExtract_GetBmps(SVGPyObj):
    xlink_img_array = SVGPyObj.g.image
    
    #pprint(xlink_img_array)
    
#    arrayBmps = []
#    for eachRect in SVGPyObj.g.rect:
#        if not(any(eachRect.id in s for s in xlink_img_array)):
#            arrayBmps.append(eachRect)
    
    return xlink_img_array 


def SVG_Construct_FlowRootRect_Pairs(SVGPyObj):
    rect_list = SVGExtract_GetRectJSON(SVGPyObj)
    flowroot_list = SVGExtract_GetTextFlowRootsJSON(SVGPyObj)    
    xlink_rects_list = SVGExtract_GetFlowRoot_Xlink_Rects(SVGPyObj)
    
    tempFlowRootTextPair = {}
    arraylist = [] 
    for eachflowroot in flowroot_list:
        tempFlowRootTextPair = {
                                'flowroot' : eachflowroot,
                                'rect'     : getRectByID(rect_list, eachflowroot.flowRegion.use.xlink_href.replace('#',''))
                                }
        arraylist.append(tempFlowRootTextPair)
    
    return arraylist
    #pprint(SVGTextList)

###################################
# Populate MHEG Object Lists      #
###################################

def Populate_MHEGRects(SVGObjList):
    global intDefineCount
    global MHEGRectList
    
    i = intDefineCount
    for eachSVGRect in SVGObjList:
        # create a mheg object
        MHEGRectObj = MHEG_Rect(eachSVGRect,i)
        i = i + 1
        MHEGRectObj.Populate()
        MHEGRectList.append(MHEGRectObj)
        
        #print MHEGRectObj.GetMHEGObjFragment()
        #print MHEGRectObj.toString()
    intDefineCount = i
    
def Populate_MHEGTexts(SVGObjList):
    global intDefineCount
    global MHEGTextList
    
    i = intDefineCount+10;
    for eachSVGText in SVGObjList:
                
        # create a mheg object
        MHEGTextObj = MHEG_Text(eachSVGText['rect'],eachSVGText['flowroot'] ,i)
        i = i + 1
        MHEGTextObj.Populate()
        MHEGTextList.append(MHEGTextObj)
    
        #print MHEGTextObj.GetMHEGObjFragment()       
    
    intDefineCount = i


def Populate_MHEGBmps(SVGObjList):
    global intDefineCount
    global MHEGBmpList
    
    i = intDefineCount+10
    for eachSVGImg in SVGObjList:
        # create a mheg object
        MHEGBmpObj = MHEG_Bmp(eachSVGImg,i)
        i = i + 1
        MHEGBmpObj.Populate()
        MHEGBmpList.append(MHEGBmpObj)
        
        #print MHEGBmpObj.GetMHEGObjFragment()
        #print MHEGRectObj.toString()
        
    intDefineCount = i

###################################
# Output MHEG-Fragments           #
###################################

def OutputMHEGFragment(zorder_list):
    global MHEGRectList
    global MHEGTextList
    global MHEGBmpList 
    
    mheg_frag = ""
    
    for eachid in zorder_list:
        if 'rect' in eachid:
            mhegobj = find_object(MHEGRectList, eachid)
            if(mhegobj != None):
                mheg_frag = mheg_frag + "\n\n" + mhegobj.GetMHEGObjFragment()
                
        elif 'flowRoot' in eachid:
            mhegobj = find_object(MHEGTextList, eachid)
            if(mhegobj != None):
                mheg_frag = mheg_frag + "\n\n" + mhegobj.GetMHEGObjFragment()
            
        elif 'image' in eachid:
            mhegobj = find_object(MHEGBmpList, eachid)
            if(mhegobj != None):
                mheg_frag = mheg_frag + "\n\n" + mhegobj.GetMHEGObjFragment()
  
    return mheg_frag
        
###################################
# Output MHEG-Define IDs          #
###################################

def GetMHEGDefineHeaderData():
    global MHEGRectList
    global MHEGTextList
    global MHEGBmpList

    mheg_defines = ""
    
    for eachobj in MHEGRectList:
        mheg_defines = mheg_defines + "$define " + eachobj.strName.replace('&','')  + "\t" + str(eachobj.intID) + "\n"
    mheg_defines = mheg_defines + "\n"
    
    for eachobj in MHEGTextList:
        mheg_defines = mheg_defines + "$define " + eachobj.strName.replace('&','')  + "\t" + str(eachobj.intID) + "\n"
    mheg_defines = mheg_defines + "\n"
    
    for eachobj in MHEGBmpList:
        mheg_defines = mheg_defines + "$define " + eachobj.strName.replace('&','')  + "\t" + str(eachobj.intID) + "\n"
    mheg_defines = mheg_defines + "\n"
    
    return mheg_defines
    
    
###################################
# Helper functions                #
###################################

def find_object(obj_list, str_id):
    for obj in obj_list:
        if obj.strID == str_id:
            return obj
    return None


def getRectByID(RectList, id):    
    for eachrect in RectList:        
        if id == eachrect.id:
            return eachrect

def pairwise(iterable):
    it = iter(iterable)
    try:
        while True:
            yield it.next(), it.next()
    except StopIteration:
        pass


def getIdsFromString(xml_str):
    
    p = re.compile('id=\"([\w-]*)\"')
    matches = p.findall(xml_str)    
    new_matches = []    
    
    # need to get only those objects we
    # are interested in
    for m in matches:
        if 'rect' in m:
            new_matches.append(m)
        elif 'flowRoot' in m:
            new_matches.append(m)
        elif 'image' in m:
            new_matches.append(m)
    
    return new_matches         
    

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


###################################
#    MAIN PROGRAM                 #
###################################
_VERSION_ = "1.3b"


print "\n**********************************************************************************"
print "\t\t SVG2MHEG - %s" % _VERSION_
print "**********************************************************************************"


usage="-i [input_svg_file] --help"    
parser = OptionParser(usage)
parser.add_option("-i", "--input", dest="input_svg_file", action="store", 
                  help="Input .svg Filename")

parser.add_option("-o", "--output_mhegF", dest="output_mhegF_file", action="store", 
                  help="Output .mhegF Filename")

parser.add_option("-d", "--output_header", dest="output_header_define_file", action="store", 
                  help="Output .h Filename")

(options, args) = parser.parse_args()

InputSVGFile = options.input_svg_file
OutputMHEGFFile = options.output_mhegF_file
OutputHeaderFile = options.output_header_define_file


# -- check for basics --
if (InputSVGFile == None) or (OutputMHEGFFile == None) or (OutputHeaderFile == None):
    print "No Input Arguments Provided"
    print usage
    sys.exit()
    
# -- first load in the svg data (as xml) --
xmldata = MISC_IO.read_file(InputSVGFile, 'r')

# -- convert to python object --
SVGPyObj = XML.xml2obj(xmldata)

# -- get print out z-order from the xml. order of which the objects
# appear in the SVG --
Z_order_list_ids = getIdsFromString(xmldata)

# -- set the define counter --
# each object has a unique id in mheg
intDefineCount = 500

# -- construct a list of MHEG Rect objects --
SVGRectList = SVGExtract_GetRects(SVGPyObj)
Populate_MHEGRects(SVGRectList)

# -- construct a list of MHEG Text objects --
# make a list of flow root + rext pairs first
SVGTextList = SVG_Construct_FlowRootRect_Pairs(SVGPyObj)
Populate_MHEGTexts(SVGTextList)

# -- construct a list of MHEG Rect objects --
SVGBmpList = SVGExtract_GetBmps(SVGPyObj)
Populate_MHEGBmps(SVGBmpList)

# -- write out complete mheg-fragment --
mhegf_outputbuff = OutputMHEGFragment(Z_order_list_ids)
MISC_IO.write_file(OutputMHEGFFile, mhegf_outputbuff)

# -- write out mheg header data : contains IDs --
mheg_defines = GetMHEGDefineHeaderData()
MISC_IO.write_file(OutputHeaderFile, mheg_defines)


#pprint(SVGPyObj.g.flowRoot)
#MISC_DEBUG.print_svg_rect(SVGPyObj)






#MISC_DEBUG.print_svg_flowRoot_XLinks(SVGPyObj)

#pprint(SVGExtract_GetFlowRoot_Xlink_Rects(SVGPyObj))
#pprint(SVGExtract_GetRects(SVGPyObj))



#print SVGPyObj.g



