# -*- coding: utf-8 -*-
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

slist=[]
infile = sys.argv[1]
with open(infile, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        slist.append(state(row[0],int(row[1])))

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# I have included several potential methods to
# determine the number of Representatives. 
#
# A: Set Number of Reps
# If you want to set the number of reps, include the
# desired number in the commandline after the csv file
#
# It will allocate the seats, if the number of seats is
# less than the number of states each will be given 1.
#       
# ex:
# >apportion.py 2010.csv 500
#
# B: Cube Root Rule
# Have the entry in the commandline after the csv file
# be the word Cube.
#
# The number of seats will be equal to the cube root of
# the total population of all states combined rounded
# to the nearest whole number.
#       
# ex:
# >apportion.py 2010.csv cube
#
# C: Wyoming Rule
# Have the entry in the commandline after the csv file
# be the word Wyoming.
#
# The number of seats will be the total population divided
# by the population of the smallest state, rounded to the
# nearest whole number.
#       
# ex:
# >apportion.py 2010.csv wyoming
#
# D: If it fails to detect one of these options it will
# default to 435.
#       
# ex:
# >apportion.py 2010.csv
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
if len(sys.argv)>2:
    method = sys.argv[2]
else:
    method = '435'

if method.isdigit():
    nreps = int(method)
elif method == "Cube" or method == "cube":
    nreps = floor((sum(st.pop for st in slist))**(1/3.)+.5)
elif method == "Wyoming" or method == "wyoming":
    slist.sort(key=lambda x: x.pop)
    nreps = floor((sum(st.pop for st in slist)/slist[0].pop)+.5)
else:
    nreps = 435 

slist.sort(key=lambda x: x.Priority,reverse=True)

out = open('Apportionment.txt','w')
out.write('Order of Seats Given:\n')

print('- '*10)
print('Last 10 Seats Given:')
for i in range(nreps - len(slist)):
    slist[0].addrep()
    if( i > nreps - len(slist) - 11):
        print(slist[0].name,end=',')
        out.write('{0:{1}}: '.format(i+len(slist)+1,len(str(nreps+10))) + slist[0].name+'\n')
        if( i == nreps - len(slist) - 1):
            out.write('- '*10+'\n')
    slist.sort(key=lambda x: x.Priority,reverse=True)
print('\n'+'- '*10)
print('Priority of States After Last Seat Given:')
statenamelist = []
for i in slist:
    print(i.name,end=',')
    statenamelist.append(i.name)
print('\n'+'- '*10)

slist.sort(key=lambda x: x.pop/x.reps,reverse=True)
popreplen=len(str(int(slist[0].pop/slist[0].reps)))+3

slist.sort(key=lambda x: x.reps,reverse=True)
replen=len(str(slist[0].reps))

repsbystatelist = []
print('Results:')
for i in slist:
    temp_str = i.name+": {0:{2}} Reps, {1:{3}.2f} pop/rep".format(i.reps,i.pop/i.reps,replen,popreplen)
    repsbystatelist.append(temp_str)
    print(temp_str)
    

print('\nRepresentatives apportioned: ',end='')
print(sum(st.reps for st in slist))

slist.sort(key=lambda x: x.Priority,reverse=True)
for i in range(10):
    slist[0].addrep()
    out.write('{0:{1}}: '.format(nreps+1+i,len(str(nreps+10))) + slist[0].name+'\n')
    slist.sort(key=lambda x: x.Priority,reverse=True)

out.write('\nPriority of States After Last Seat Given:\n')
itt = 1
for name in statenamelist:
    out.write('{0:02d}:'.format(itt)+name+'  ')
    if(itt%5 == 0):
        out.write('\n')
    itt+=1
out.write('\nResults:\n')
for entry in repsbystatelist:
    out.write(entry+'\n')

out.close()