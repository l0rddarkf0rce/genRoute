############################################################
# Program Name:  genRoute.py
# Version:       2.0
# Author:        L0rd DarkF0ce
# GitHub:        https://github.com/l0rddarkf0rce/genRoute
# Date Created:  20210206
# Last Modified: 20200209
############################################################

import os
import sys, getopt

inFile = ''
outFile = ''
ERROR1 = 'Invalid number of parameters'
ERROR2 = 'Invalid parameter provided'
ERROR3 = 'ERROR: In file ({}) does not exists.'
ERROR4 = 'ERROR: Out file ({}) already exists.'

def usage(name, msg):
   print('ERROR: {}\n   Usage: {} -i <INPUTFILE> -o <OUTFILE>\n'.format(msg, name))

def trunc(fn):
   lines = open(fn, 'r').readlines()
   lastLine = (lines[-1].rstrip())
   lines[-1] = lastLine
   open(fn, 'w').writelines(lines)
   return 0

def find_nth(myString, mySubString, n):
   if (n == 1):
       return myString.find(mySubString)
   else:
       return myString.find(mySubString, find_nth(myString, mySubString, n -1) + 1)

def findQuest(quest, questList):
   n = -1
   for x in range(len(questList)):
       key = questList[x][0]
       
       if quest == key:
           return x
   return n

def main():
   tmpFile = 'foobar'
   Quests = []

   # Read quests.txt file and only keep the coordinates
   with open(inFile, 'r') as f:
      line = f.readline()
      while line:
         n = find_nth(line, ' ', 2) + 1
         coords = line[line.find(' ') + 1:n - 1]
         qName = line[n:].rstrip().replace(':', ' -').replace(' ', '_')
         questNumber = findQuest(qName, Quests)
         if questNumber == -1:
            Quests.append(['',''])
            Quests[len(Quests) - 1][0] = qName
            Quests[len(Quests) - 1][1] = coords
         else:
            Quests[questNumber][1] += ';' + coords
         line = f.readline()
   
   for quest in Quests:
      with open(quest[0]+'.txt', 'w') as f:
         qCoords = quest[1].split(';')
         for x in range(len(qCoords)):
            print(qCoords[x], file=f)

      # Generate optimized GPX file
      # For some un-Godly reason I have to remove the last new line from the file. This seems to be a
      # bug with the library used to generate the optimized gpx route. I contacted the developer but
      # have not received any answers. At some point I may look at fixing it myself, but for now this hack
      # will do the trick.
      # 
      # The library can be found at https://gitlab.com/3nvy/gpx-route-generator-console
      ret_code = trunc(quest[0]+'.txt')
      ret_code = os.system('node generate in='+quest[0]+'.txt out='+quest[0]+' type=2OPT count=50')
      
      # Process GPX file
      with open(quest[0]+'.gpx') as f:
         lines = [line.strip() for line in f if line.startswith('<wpt')]

      with open(quest[0]+'.out', 'w') as f:
         for line in lines:
            lat = line.split(' ')[1].split('"')[1]
            lon = line.split(' ')[2].split('"')[1]
            print("{},{}".format(lat,lon), file=f)

      ret_code = os.system('del '+quest[0]+'.txt '+quest[0]+'.gpx')
      print('{} generated'.format(quest[0]+'.out'))

def filesOK():
   code = True

   if not os.path.isfile(inFile):
      print(ERROR3.format(inFile))
      code = False

   if os.path.isfile(outFile):
      print(ERROR4.format(outFile))
      code = False

   return code

if __name__ == '__main__':
   if (len(sys.argv) < 3):
      usage(sys.argv[0], ERROR1)
      sys.exit(1)

   fCmd = sys.argv
   argList = fCmd[1:]
   sOptions = 'i:'
   try:
      args, vals = getopt.getopt(argList, sOptions)
   except getopt.error as err:
      usage(fCmd[0], err)
      sys.exit(1)

   for cArg, cVal in args:
      if cArg in ('-i'):
         inFile = cVal
      else:
         usage(fCmd[0], ERROR2)

   if filesOK():
      main()
      sys.exit(0)
   else:
      sys.exit(1)
