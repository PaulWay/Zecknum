# Zecknum
Convert numbers to and from Zeckendorf representation, using Fibonacci bases.

# Simple description

Put simply, Zeckendorf representation is a maximally efficient 
self-terminating encoding for whole numbers (integers > 0).  Each 
representation ends with '11', and '11' cannot appear anywhere in a 
representation (due to the way the representation is constructed).  Smaller 
numbers get smaller representations, so it's good for representing values 
such as array numbers, object IDs and other identifiers that are usually 
numbered from 1.

# Functions

```Python
Zecknum.to_zeck(44)
'010010011'
```

Converts a number to its Zeckendorf representation.

```Python
Zecknum.from_zeck('1000101000101001101011')
33156
```

Converts a Zeckendorf representation to its numeric equivalent.
