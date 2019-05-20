#!/usr/bin/python
import json
import sys


filepath =  sys.argv[1] 
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
   	   print line["notifications"][0]["locationCoordinate"]["x"]
       print("Line {}: X {}".format(cnt, line["notifications"][0]["locationCoordinate"]["x"]))
       print("Line {}: Y {}".format(cnt, line["notifications"][0]["locationCoordinate"]["Y"]))
       line = fp.readline()
       cnt += 1