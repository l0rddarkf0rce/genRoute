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

def main():
   tmpFile = 'foobar'
   coords = []

   # Read quests.txt file and only keep the coordinates
   with open(inFile) as f:
      line = f.readline()
      while line:
         coords.append(line.split(' ')[1])
         line = f.readline()

   with open(tmpFile+'.txt', 'w') as f:
      for line in coords:
         print(line, file=f)

   # Generate optimized GPX file
   # For some un-Godly reason I have to remove the last new line from the file
   #ret_code = os.system('truncate -s -1 '+tmpFile+'.txt')
   ret_code = trunc(tmpFile+'.txt')
   ret_code = os.system('node generate in='+tmpFile+'.txt out='+tmpFile+' type=2OPT count=50')

   # Process GPX file
   with open(tmpFile+'.gpx') as f:
      lines = [line.strip() for line in f if line.startswith('<wpt')]

   with open(outFile, 'w') as f:
      for l in lines:
         lat = l.split(' ')[1].split('"')[1]
         lon = l.split(' ')[2].split('"')[1]
         print("{},{}".format(lat,lon), file=f)

   ret_code = os.system('del '+tmpFile+'.txt '+tmpFile+'.gpx')
   print('{} generated'.format(outFile))

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
