import xml.etree.ElementTree as ET
import re
import pprint
import sys
import urllib2


tagList = ['id', 'published', 'updated', 'title', 'name', 'uri', 'email', 'nickname', 'thumbnail', 'user', 'version', 'albumid', 'access', 'width', 'height', 'size', 'client', 'checksum', 'timestamp', 'imageVersion', 'commentingEnabled', 'commentCount', 'license', 'fstop', 'make', 'model', 'exposure', 'flash', 'focallength', 'time', 'imageUniqueID', 'credit', 'keywords', 'albumtitle', 'albumctitle', 'snippettype', 'truncated', 'iso', 'albumdesc', 'location', 'pos', 'distance', 'summary', 'description', 'position', 'videostatus']


def getTag(node):
  tag = re.sub("{.*}", '', node.tag)
  return tag
  
def printNode(node, params):
  print "%s : %s" % (getTag(node), node.text),

def addTags(node, tagList):
  tag = getTag(node)
  if tag in tagList : pass
  else :
    tagList.append(tag)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
def removeCommas(s): return "".join(i for i in s if ord(i)!=44)

def extractTags(node, entryData):
  tag   = getTag(node)
  try:
    index = tagList.index(tag)
    entryData[index] = removeCommas(removeNonAscii(node.text))
  except ValueError:
    print "Error (%s) %s"  % (node.text, tag)


def traverse(node,func,params):
  if len(node) == 0 :
    if node.text is None : pass
    else :
      func(node,params)
  else:
    for subnode in node:
      traverse(subnode,func,params)


def main():

  if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s picasa-url \n" % sys.argv[0])
    return


  picasaURL  = sys.argv[1]
  try: 
    req = urllib2.Request(picasaURL)
    res = urllib2.urlopen(req)
  except IOError:
    print "Not a valid URL"

  exif_ns    = "http://schemas.google.com/photos/exif/2007"
  default_ns = 'http://www.w3.org/2005/Atom'

  tree       = ET.parse(res)
  entries    = tree.findall('.//{%s}entry' % default_ns)

  allEntries = []
  for entry in entries: 
    entryData = ['' for x in tagList]
    allEntries.append(entryData)
    traverse(entry, extractTags, entryData)

  #
  # print csv format
  #

  tagString = ",".join(x for x in tagList)
  print tagString

  for entry in allEntries : 
    for val in entry : print val, 
    entryString = ",".join(x for x in entry)
    print entryString


  #
  # For histogramming. Not yet working.
  #

  pp = pprint.PrettyPrinter(indent=2)
  plotList = ['focallength', 'exposure', 'make', 'model', 'iso', 'fstop']

  attributes = []
  for index in range(0,len(tagList)):
    vals = {}
    attributes.append(vals)
    for entry in allEntries:
      key = entry[index]
      if key == '': key = 'none'
      if key in vals:
        vals[key] =  vals[key]+1
      else:
        vals[key] = 1

  for index in range(0,len(tagList)):
    if tagList[index] not in plotList:
      continue 
    #print "%s :" % tagList[index],
    #pp.pprint( attributes[index] )

if __name__ == '__main__':
   main()
