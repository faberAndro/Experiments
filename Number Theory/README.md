PLOT BINARY PRIMES:

In order to run, this file requires the matplotlib module to be installed.

The first 23000 prime numbers are visualized as leaves of a binary tree, 
to check for any repetitive pattern to exist. 
Only leaves are displayed, not branches. 
The binary tree starts at the left bottom corner and expands towards NE. 
Every red imaginary line represents a bunch of numbers laying between 2^n and 2^(n-1) 
The blue line represents the horizon of infinites. 
For the numbers to be visualized close to the horizon, 
at least the first 2^40 numbers need to be primality tested. 
The current parameters are set for the first 2^18 numbers to be primality tested. 
Prime numbers are here generated through the ancient Eratosthenes' sieve algorithm. 
The "power" parameter (18) can be changed, but some reductions factors apply to keep the graph able to run. 
To investigate the leaves pattern, the graph can be zoomed.