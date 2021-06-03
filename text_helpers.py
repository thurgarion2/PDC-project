import numpy as np
import ghw2_encoder as encoder

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

def byte_array_to_channel_format(byte_array):
    return bit_array_to_channel_format(to_bit_array(byte_array))

def channel_format_to_byte_array(channel_format):
    return to_byte_array(channel_format_to_bit_array(channel_format)).tobytes()

def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    out = chanInput + np.sqrt(10)*np.random.randn(len(chanInput))
    return out

def encode_file(input, output, encoder):
    with open(input, 'rb') as f:
        data = f.read()
        print(len(data))
        encoded = encoder.encode(byte_array_to_channel_format(data))
        print(encoded.size)
        np.savetxt(output, encoded)


def decode_file(input, output, encoder):
    with open(output, 'wb') as f:
        data = np.loadtxt(input)
        decoded = channel_format_to_byte_array(encoder.decode(data))
        f.write(decoded)


def hamming_distance(a, b):
    return np.sum(np.where(a-b != 0, 1, 0))

    
if __name__ == '__main__':
    encoder = encoder.encoder()
    text = './80_character.txt'

    ##encoding='utf-8'
    with open(text, 'rb') as f:
        data = f.read()

        channel_format = byte_array_to_channel_format(data)
        
        tot = 0
        for loop in range(100):
            output = channel(encoder.encode(channel_format))
            decoded = encoder.decode(output)
            text = channel_format_to_byte_array(decoded)
            tot = tot + hamming_distance(channel_format,decoded)
            print(loop)

        print("{} avg".format(tot/100))

       
    
