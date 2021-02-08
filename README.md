# genRoute

I created this to help in generating route paths for different Field Research tasks. I took the great work that BlisseyBuster started and just automated them with python. I wrote it so that it would work on Windows 10 and have tested it only on my system. Hopefully the instructions bellow will help to get this running.

To get the original instructions created by BlisseyBuster go to https://www.reddit.com/r/PokemonGoSpoofing/comments/ldck91/how_i_create_lists_of_research_task_coords/

## Requirements
1. Python 3.9 or better (https://www.python.org/downloads/windows/)
2. node.js (https://nodejs.org/en/download/) I used the Windows 64-bit msi, but you get the one you need
3. git install (since node.js install chocolatey you can use chocolatey to install this) (https://chocolatey.org/packages/git.install)
4. Renato Pestana's GPX Route Generator Console (https://gitlab.com/3nvy/gpx-route-generator-console)

## Instructions
1. Install python.
2. Install node.js.
3. Install Git Install.
4. Download GPX Route generator. Follow the instructions for it it is straight forward and simple.
5. Download genRoute and copy it to the same folder where GPX Route Generator is.
6. Follow the instructions that BlisseyBuster wrote to create lists of research task coordinates and stop after Step 1.
7. Feed the file that you created on step 6 above to feed genRoute the output for your route will be in the file you specify.
8. Take the ruslting file and go back to BlisseyBuster instructions and copy and paste into the spreadsheet he created.

## Command line parameters
* -i INPUTFILE. This is the file name that you generated on step 6 above
* -o OUTFILE. This is the filename that you want the results to be saved to.

### Example

```python
python genRoute -i route.txt -o optimized-route.txt
```

Hopefully this all works for you!
