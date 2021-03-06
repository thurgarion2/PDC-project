import numpy as np

#get if the bit is 0 or 1
def access_bit(data, num):
    shift = int(num % 8)
    return (data & (1<<shift)) >> shift

#translate to bit array
def to_bit_array(byte_array):
    bits = []

    for byte in byte_array:
        for i in range(8):
            bits.append(access_bit(byte, i))
    return np.array(bits)

#return byte array
def to_byte_array(bit_array):
    return np.packbits(bit_array, bitorder='little')

# 1 -> 1
# 0 -> -1
def bit_array_to_channel_format(bit_array):
    return 2*np.array(bit_array) - 1

# 1 -> 1
# -1 -> 0
#(no noise)
def channel_format_to_bit_array(bit_array):
    return (np.array(bit_array) + 1) // 2


##########################################################
##########################################################

####### transfrom file to channel format
####### we still need to add encoding and decoding
####### channel format is numpy array composed of -1 and 1
####### ex : [-1, 1, 1, -1, 1, 1, 1, -1]

#Returns array in the Channel format from byte array
def byte_array_to_channel_format(byte_array):
    return bit_array_to_channel_format(to_bit_array(byte_array))

#Returns byte format array from the channel format
def channel_format_to_byte_array(channel_format):
    return to_byte_array(channel_format_to_bit_array(channel_format)).tobytes()

#Channel transformation
def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))
    
#Calculate hammming distance
def hamming_distance(a, b):
    return np.sum(np.where(a-b != 0, 1, 0))