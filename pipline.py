import numpy as np
import repeat_and_discard as encoder

def access_bit(data, num):
    shift = int(num % 8)
    return (data & (1<<shift)) >> shift

def to_bit_array(byte_array):
    bits = []

    for byte in byte_array:
        for i in range(8):
            bits.append(access_bit(byte, i))
    return np.array(bits)

def to_byte_array(bit_array):
    return np.packbits(bit_array, bitorder='little')

## 1 -> 1
## 0 -> -1
def bit_array_to_channel_fromat(bit_array):
    return 2*np.array(bit_array) - 1

#(no noise)
def channel_fromat_to_bit_array(bit_array):
    return (np.array(bit_array) + 1) // 2


##########################################################
##########################################################

####### transfrom file to channel fromat
####### we still need to add encoding and decoding
####### channel fromat is numpy array composed of -1 and 1
####### ex : [-1, 1, 1, -1, 1, 1, 1, -1]

def byte_array_to_channel_fromat(byte_array):
    return bit_array_to_channel_fromat(to_bit_array(byte_array))

def channel_fromat_to_byte_array(channel_fromat):
    return to_byte_array(channel_fromat_to_bit_array(channel_fromat)).tobytes()

def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))



if __name__ == '__main__':
    encoder = encoder.encoder(80)
    text = './80_character.txt'

    ##encoding='utf-8'
    with open(text, 'rb') as f:
        data = f.read()
   
        channel_format = byte_array_to_channel_fromat(data)
        output = channel(encoder.encode(channel_format))
        text = channel_fromat_to_byte_array(encoder.decode(output))

        print(text == data)
        print(text.decode())
    
