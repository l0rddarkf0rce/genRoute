############################################################
# Program Name:  genRoute.py
# Version:       2.6
# Author:        L0rd DarkF0ce
# GitHub:        https://github.com/l0rddarkf0rce/genRoute
############################################################
# 20210206
#    Original program created
#
# 20200209
#    Added code to create different files for each of the
#    research tasks.
#
# 20200210
#    Added code to calculate and print distance and cool
#    down times.
# 20200213
#    Added code to combine the quests into one single file
#    and format the file to paste into Reddit.
############################################################

import os
import sys, getopt
from math import sin, cos, sqrt, atan2, radians

inFile = ''
outFile = ''
ERROR1 = 'Invalid number of parameters'
ERROR2 = 'Invalid parameter provided'
ERROR3 = 'ERROR: In file ({}) does not exists.'
ERROR4 = 'ERROR: Out file ({}) already exists.'

def combine(iFile, oFile):
   '''
   **Catch 1 Pokemon (Type - Dragon) - 10 Ultra Balls** 
   * \[1.392315, 103.916264\]
   * \[1.393947, 103.886417\] distance 3.33 km - cooldown 1.5 min
   * \[1.313657, 103.785238\] distance 14.38 km - cooldown 8 min

   **Catch 1 Pokemon (Type - Dragon) - 1500 Stardust** 

   * \[1.291691, 103.847889\]
   * \[1.366582, 103.75204\] distance 13.54 km - cooldown 8 min
   * \[1.279148, 103.838751\] distance 13.71 km - cooldown 8 min
   '''
   with open(iFile, 'r') as f:
      # do something here
      lines = f.readlines()
      title = '**'+iFile[:-4].replace('_', ' ').replace('Gible', 'G.i.b.l.e.')+'**'
      with open(oFile, 'a') as of:
         print(title, file=of)
         for line in lines:
            print('* {}'.format(line.replace('[', '\[').replace(']', '\]')), file=of)

def coolDown(file):
   coords = []
   cd = {0: '15 sec',
         1: '30 sec',
         2: '1 min',
         3: '1.5 min',
         4: '1.5 min',
         5: '2 min',
         6: '3 min',
         7: '5 min',
         8: '6 min',
         9: '6 min',
         10: '7 min',
         11: '7 min',
         12: '8 min',
         13: '8 min',
         14: '8 min',
         15: '9 min',
         16: '9 min',
         17: '9 min',
         18: '10 min',
         19: '10 min',
         20: '11 min',
         21: '11 min',
         22: '12 min',
         23: '12 min',
         24: '13 min',
         25: '14 min',
         26: '15 min',
         27: '15 min',
         28: '15 min',
         29: '16 min',
         30: '16 min'}

   with open(file, 'r') as f:
      for line in f.readlines():
         f_list = [float(i) for i in line.split(',') if i.strip()]
         coords.append(f_list)

   with open(file, 'w') as f:
      # write back to the file
      print(coords[0], file=f)
      for x in range(1, len(coords)):
         dist = distance(coords[x-1],coords[x])
         print('{} distance {} km - cooldown {}'.format(coords[x], round(dist, 2), cd[round(dist, 0)]), file=f)

def usage(name, msg):
   # Parameters:
   #    name: string containing the name of the program itself
   #    msg: string of the error message that we want to print
   # Description:
   #    Print usage message for our program
   print('ERROR: {}\n   Usage: {} -i <INPUTFILE> -o <OUTFILE>\n'.format(msg, name))

def trunc(fn):
   # Parameters:
   #    fn: filename that we want to truncate the last line for
   # Description:
   #    Removes the NL character from the last line of the file
   lines = open(fn, 'r').readlines()
   lastLine = (lines[-1].rstrip())
   lines[-1] = lastLine
   open(fn, 'w').writelines(lines)
   return 0

def find_nth(myString, mySubString, n):
   # Parameters
   #    myString: string that we will look in
   #    mySubString: string that we will look for inside of myString
   #    n: integer represent the # of the occurence of mySubString insode of myString
   # Return:
   #    If found, return the location of the nth occurence of mySubString inside of myString
   if (n == 1):
       return myString.find(mySubString)
   else:
       return myString.find(mySubString, find_nth(myString, mySubString, n -1) + 1)

def findQuest(quest, questList):
   # Parameters:
   #    quest: string representing the quest that we are looking for
   #    questList: Array of all of the available quests
   # Return:
   #    If found, the possition in the array
   n = -1
   for x in range(len(questList)):
       key = questList[x][0]
       
       if quest == key:
           return x
   return n

def distance(c1, c2):
    # Parameters:
    #    c1: tuple of float (lat, lon)
    #    c2: tuple of float (lat, lon)
    # Return:
    #    Distance in km between c1 and c2: float
    
    # Earth's radius at the equator in KM
    R = 6378.0

    lat1, lon1 = c1
    lat2, lon2 = c2
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = ((sin(dlat / 2)**2) + ((cos(radians(lat1)) * cos(radians(lat2))) * (sin(dlon / 2)**2)))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    
    return(d)

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

      # Calculate distance
      coolDown(quest[0]+'.out')

      combine(quest[0]+'.out', outFile)
      
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
   if (len(sys.argv) < 5):
      usage(sys.argv[0], ERROR1)
      sys.exit(1)

   fCmd = sys.argv
   argList = fCmd[1:]
   sOptions = 'i:o:'

   try:
      args, vals = getopt.getopt(argList, sOptions)
   except getopt.error as err:
      usage(fCmd[0], err)
      sys.exit(1)

   for cArg, cVal in args:
      if cArg in ('-i'):
         inFile = cVal
      elif cArg in ('-o'):
         outFile = cVal
      else:
         usage(fCmd[0], ERROR2)

   if filesOK():
      main()
      sys.exit(0)
   else:
      sys.exit(1)