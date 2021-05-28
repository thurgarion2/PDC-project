import numpy as np

# constructs C_n given n
def construct_c(n, c_0):
    if n == 0:
        return c_0   
    c_n = []
    for i in range(n):
        c_i = []
        for c in c_0:
            c_i.append(np.block([c,c]))
            c_i.append(np.block([c, -c]))
        c_n = construct_c(i, c_i)
    return c_n

# constructs all possible bit permutation of length n
def per(n):
    permutations = []
    for i in range(1 << n):
        s = bin(i)[2:]
        s = '0' * (n - len(s)) + s
        permutations.append(s)
    return permutations

# constructs the map from bit sequence of length n (string, ex: '010') to codeword of length 2^n (ex: [1, -1, 1, -1, 1, -1, 1, -1])
def mapping(n):
    permutations = per(n)
    codewords = construct_c(n, [1])

    map = {}
    for i in range(pow(2,n)):
        map.update({permutations[i]: codewords[i]})

    return map

# encodes blocks of bits of length n 
# bits is a string of bits 0 and 1
def encode(bits, n):
    map = mapping(n)
    sequence = []
    for b in range(0, len(bits), n):
        sequence.append(map.get(bits[b:b+n]))
    return np.concatenate(sequence)



    






