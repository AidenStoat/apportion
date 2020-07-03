#Seat apportionment

This script implements the Method of Equal Proportions used to determine the apportionment of seats in the House of Representatives to the US states.  It is written for python 3.7, I have not tested it with older versions.

Requires input from a csv file with each line representing a state and formatted as: 
	Name, population
*see examples like 2010.csv

I have designed it to run from command line in this format:
	>python3 apportion.py [csv_file] [Number_of_seats (optional)]

The US House of Representatives is currently capped at 435 seats.  The script will automatically apportion 435 seats unless given a different number.  Above, the 'Number_of_seats' option can be any integer number, if left blank or an invalid value is given it will default to 435.
	>python3 apportion.py 2010.csv
	>python3 apportion.py 2010.csv 517

I also implemented two methods of choosing a number.
The Wyoming rule states that the average population represented by each seat should match the population of the smallest state.  This script takes the total population divided by the population of the smallest state to get the number of seats. Write 'wyoming' instead of a number.
	>python3 apportion.py 2010.csv wyoming

The Cube Root rule notes that the number of seats in national legislatures roughly corelate with the cube root of the total population, thus calculates the cube root to get the number of seats.  Write 'cube' instead of a number.
	>python3 apportion.py 2010.csv cube

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

The method of apportionment is called the Method of Equal Proportions.
Each state starts with its guaranteed 1 seat and has a priority value based on population and current number of seats.  The rest of the seats are given out, one at a time, to the state with the highest priority.  The priority, An, is determined by the ratio of the state population, P, to the geometric mean of its current number of seats, n, and the number one seat higher.
An = P / sqrt(n*(n+1))

This method is used because it minimizes the percentage difference in population of each Congressional District.  It does this while avoiding the Alabama paradox of previous methods where a state could lose a seat in congress when new seats were added.

My script uses the equivalent recursive form of this.  The priority after adding a seat can be found by multiplying the current priority by sqrt( n / n+2 ).
