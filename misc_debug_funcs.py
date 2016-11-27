from pprint import pprint
import os, sys
import shutil


def print_svg_rect(SVGPyObj):
    pprint(SVGPyObj.g.rect)
    
def print_svg_text(SVGPyObj):
    pprint(SVGPyObj.g.text)
    
    
def print_svg_flowRoot(SVGPyObj):
    arrayList = []

    for eachflowRoot in SVGPyObj.g.flowRoot:                
        if(eachflowRoot.flowRegion.use != None):
            arrayList.append(eachflowRoot)
            
    pprint(arrayList)
    #return arrayList

def print_svg_flowRoot_XLinks(SVGPyObj):
    arrayList = []

    for eachflowRoot in SVGPyObj.g.flowRoot:                
        if(eachflowRoot.flowRegion.use != None):
            arrayList.append(eachflowRoot.flowRegion.use.xlink_href)
            
    pprint(arrayList)
    #return arrayList