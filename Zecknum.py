#!/usr/bin/python
# vim: set ts=4 et ai:

import math

"""
    Produce Zeckendorf representations of a number.  This is the reverse
    of the Fibonacci-base binary representation of the number, with a '1'
    appended to indicate the end of the representation.
"""

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

def fib_seq_num_greater(f_n): 
    """
        The sequence position of the fibonacci number greater than f_n.
        We subtract one because our sequence actually starts at the second
        fibonacci number.
    """
    return int(math.log(f_n*sqrt5+1, phi)-1)

def to_zeck(num):
    """
        Convert a number to a zeckendorf representation.
        If we don't have the representation already cached, calculate it
        
    """
    if num in zeck_rep:
        return zeck_rep[num]
    
    # Find the position in the array of Fibonacci number greater than num
    pos = fib_seq_num_greater(num)
    
    # If the last was still not large enough, generate some more    
    while pos > len(fib_seq):
        fib_seq.append(fib_seq[-2]+fib_seq[-1])
        
    # Greedy algorithm to generate the representation string
    rep = ''
    current = num
    while pos > 0:
        pos -= 1 # decrement first since previous was greater than req.d
        fib = fib_seq[pos]
        if current >= fib:
            rep += '1'
            current -= fib
        else:
            rep += '0'
        if current == 0:
            break
    if pos > 0:
        rep += ('0' * pos)
    
    # Turn it around, add the suffix, remember it and return it
    rev = rep[::-1] + '1'
    zeck_rep[num] = rev
    num_rep[rev] = num
    return rev

def from_zeck(zeck):
    """
        Convert a Zeckendorf representation to a number.
        Check that it is one, but then work upward from the first digit
        (the least is now at the front) adding Fibonacci numbers until we
        hit the end.
    """
    if zeck[-2:] != '11':
        return False
    if zeck in num_rep:
        return num_rep[zeck]
    
    pos = 0
    num = 0
    for bit in zeck[:-1]:
        val = fib_seq[pos]
        if bit == '1':
            num += val
        pos += 1
    
    # If we didn't look it up, it's not in either cache, so cache it
    zeck_rep[num] = zeck
    num_rep[zeck] = num
    return num

