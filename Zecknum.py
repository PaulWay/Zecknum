#!/usr/bin/python
# vim: set ts=4 et ai:

import math

"""
    Produce Zeckendorf representations of a number.  This is the reverse
    of the Fibonacci-base binary representation of the number, with a '1'
    appended to indicate the end of the representation.
"""

class InvalidRepresentation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# The fibonacci sequence numbers so far
fib_seq = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, ]
# A cache for previously calculated representations
zeck_rep = {1: '11', 2: '011', 3: '0011', 4: '1011', 5: '00011', 6: '10011', 
 7: '01011', 8: '000011', 9: '100011', 10: '010011', 11: '001011', 12: '101011',
 13: '0000011', 14: '1000011', 15: '0100011', 16: '0010011', 17: '1010011',
 18: '0001011', 19: '1001011', 20: '0101011',}
num_rep = { v: k for k, v in zeck_rep.items() }

# Phi is the limit of the ratio between two adjacent fibonacci numbers.
# So it's possible to work out which term in the fibonacci sequence a number
# is nearest / just above / just below using Phi.  Thanks to sleepingsquirrel
# in https://www.reddit.com/r/dailyprogrammer/comments/wa0mc/792012_challenge_74_easy/
# for the reminder of how to do this.
sqrt5 = math.sqrt(5)
phi = (1+sqrt5)/2

def fib_pos_no_greater_than(f_n):
    """
        The sequence position of the fibonacci number greater than f_n.
        We subtract one because our sequence actually starts at the second
        fibonacci number.  log(f_n*sqrt5+1) only goes up
    """
    return int(math.log((f_n+1)*sqrt5+1, phi))-2

def to_zeck(num):
    """
        Convert a number to a zeckendorf representation.
        If we don't have the representation already cached, calculate it
        
    """
    if num < 1:
        raise ValueError(str(num) + " is too small to convert to Zeckendorf representation - must be >= 1")
    if num in zeck_rep:
        return zeck_rep[num]
    
    # Find the position in the array of Fibonacci number greater than num
    pos = fib_seq_num_just_less(num)
    
    # If the last was still not large enough, generate some more    
    while pos > len(fib_seq):
        fib_seq.append(fib_seq[-2]+fib_seq[-1])
        
    # Greedy algorithm to generate the representation string, but iterate via
    # remaining sum rather than per position.
    rep = '11' # suffix
    current = num - fib_seq[pos] # Start after the first iteration
    while current > 0:
        # Instead of decrementing, work out the next Fibonacci number less
        # than the current (it'll be before the result from
        # fib_seq_num_greater()).  Then add zeros for the numbers we skipped.
        new_pos = fib_seq_num_just_less(current)
        # Construct the string by prepending rather than appending.  Efficient?
        # Also, lessen number of zeros by one of fencepost error - number of
        # zeros between positions 4 and 2 is one, not two.
        rep = '1' + '0' * (pos - (new_pos+1)) + rep
        current -= fib_seq[new_pos]
        pos = new_pos
    if pos > 0:
        rep = '0' * pos + rep
    
    # remember it and return it
    zeck_rep[num] = rep
    num_rep[rep] = num
    return rep

def from_zeck(zeck):
    """
        Convert a single Zeckendorf representation to a number.
        Check that it is one, but then work upward from the first digit
        (the least is now at the front) adding Fibonacci numbers until we
        hit the end.
    """
    if zeck[-2:] != '11':
        raise InvalidRepresentation(zeck)
    if zeck.strip('01'):
		raise InvalidRepresentation(zeck)

    # If the string contains multiple zecknums, return an array of each
    # individual representation as a number.
    if '11' in zeck[0:-1]:
		return [from_zeck(x + '11') for x in zeck.split('11') if x]

    if zeck in num_rep:
        return num_rep[zeck]
    
    num = 0
    for pos, bit in enumerate(zeck[:-1]):
        # Extend the sequence if we need more:
        if pos == len(fib_seq):
            fib_seq.append(fib_seq[-2]+fib_seq[-1])
        if bit == '1':
            num += fib_seq[pos]
    
    # If we didn't look it up, it's not in either cache, so cache it
    zeck_rep[num] = zeck
    num_rep[zeck] = num
    return num

