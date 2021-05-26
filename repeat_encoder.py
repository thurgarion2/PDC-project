from typing import Sequence
import numpy as np

#bits is a sequence of -1, 1
def encode(bits, n):
    sequence = []

    for b in bits:
        sequence.append(np.ones((n))*b) 
    return np.concatenate(sequence)

def dist(arrays, array):
    return  np.sum((arrays - array)**2, axis = 0)

def decode(sequence, n):
    nb_blocks = sequence.size/n
    blocks = np.split(sequence, nb_blocks)

    possible_sequence = np.ones((n,2))
    possible_sequence[:,1] = - possible_sequence[:,1]
    choice_to_bit = {0 : 1, 1 : -1}
    
    reconstructed = []
    for block in blocks:
        block = block.reshape((-1,1))
        choice = np.argmin(dist(possible_sequence, block))
        reconstructed.append(choice_to_bit[choice])
    
    return np.array(reconstructed, dtype= int)

    

if __name__ == '__main__':
    array = np.array([1,-1,1,-1])
    channel = encode(array, 4)
    print(channel)
    print(decode(channel, 4))