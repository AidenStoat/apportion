"""
Created on Mon Nov 28 16:35:10 2016

@author: Kyle
"""

import sys
from math import sqrt
from math import floor
import csv

class state(object):
    
    def __init__(self,name,pop):
        self.name=name
        self.pop=pop
        self.Priority=pop/sqrt(2)
        self.reps=1
    
    def addrep(self):
        self.Priority=sqrt(self.reps/(self.reps+2))*self.Priority
        self.reps+=1

# Read data from csv file
slist=[]
infile = sys.argv[1]
with open(infile, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        slist.append(state(row[0],int(row[1])))

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# I have included several potential methods to
# determine the number of Representatives. 
# - - -
# A: Set Number of Reps
# If you want to set the number of reps, include the
# desired number in the command line after the csv filename
#
# It will allocate the seats, if the number of seats is
# less than the number of states each will still be given 1.
#       
# ex:
# >python3 apportion.py 2010.csv 500
# - - -
# B: Cube Root Rule
# Have the entry in the command line after the csv file
# be the word cube.
#
# The number of seats will be equal to the cube root of
# the total population of all states combined rounded
# to the nearest whole number.
#       
# ex:
# >python3 apportion.py 2010.csv cube
# - - -
# C: Wyoming Rule
# Have the entry in the command line after the csv file
# be the word Wyoming.
#
# The number of seats will be the total population divided
# by the population of the smallest state (not necessarily Wyoming),
# rounded to the nearest whole number.
#       
# ex:
# >python3 apportion.py 2010.csv wyoming
# - - -
# D: If it fails to detect one of these options it will
# default to 435, the current size.
#       
# ex:
# >python3 apportion.py 2010.csv
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Choose the number of reps to apportion
if len(sys.argv)>2:
    method = sys.argv[2]
else:
    method = '435'

if method.isdigit():
    nreps = int(method)
elif method.lower() == "cube":
    nreps = floor((sum(st.pop for st in slist))**(1/3.)+.5)
elif method.lower() == "wyoming":
    slist.sort(key=lambda x: x.pop)
    nreps = floor((sum(st.pop for st in slist)/slist[0].pop)+.5)
else:
    nreps = 435

# create file to output to named Apportionment_{csv filename}.txt
out = open('Apportionment_{}.txt'.format(infile[:-4]),'w')

# Loop through the states, adding one representative at a time
# until the desired number have been apportioned.
print('- '*10)
print('Last 10 Seats Given:')
out.write('Order of Seats Given:\n')
for i in range(nreps - len(slist)):
    slist.sort(key=lambda x: x.Priority,reverse=True)
    slist[0].addrep()
    out.write(slist[0].name+', ')
    if( i > nreps - len(slist) - 11):
        print(slist[0].name,end=',')          
print('\n'+'- '*10)
out.write('\n'+'- '*10+'\n')

# Show state names in order of highest to lowest priority.
print('Priority of States After Last Seat Given:')
out.write('Priority of States After Last Seat Given:\n')
slist.sort(key=lambda x: x.Priority,reverse=True)  
for i in slist:
    print(i.name,end=',')
    out.write(i.name+', ')
print('\n'+'- '*10)
out.write('\n'+'- '*10+'\n')

# Get string lengths for formatting results
slist.sort(key=lambda x: x.pop/x.reps,reverse=True)
popreplen=len(str(int(slist[0].pop/slist[0].reps)))+3
slist.sort(key=lambda x: x.reps,reverse=True)
replen=len(str(slist[0].reps))

# Display results
print('Results:')
out.write('Results:\n')
for i in slist:
    temp_str =i.name+": {0:{2}} Reps, {1:{3}.2f} pop/rep".format(i.reps,i.pop/i.reps,replen,popreplen)
    print(temp_str)
    out.write(temp_str+'\n')

# Display total number of representatives
print('\nRepresentatives apportioned: {}'.format(nreps),end='')
out.write('\nRepresentatives apportioned: {}'.format(nreps))
out.close()