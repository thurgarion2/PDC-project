import numpy as np
import argparse
import pathlib
import ghw2_encoder as encoder
import pipeline_helper as ph
import client


def parse_args():
    parser = argparse.ArgumentParser(description="COM-302 black-box channel simulator. (client)",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="To promote efficient communication schemes, transmissions are limited to 1 Mega-sample.")

    parser.add_argument('--input_file', type=str, required=True,
                        help='.txt file')
    parser.add_argument('--output_file', type=str, required=True,
                        help='.txt file to which encoded/decoded file is saved.')
    parser.add_argument('--mode', type=str, required=True,
                        help='"encode", "decode" or "test"')

    args = parser.parse_args()

    args.input_file = pathlib.Path(args.input_file).resolve(strict=True)
    if not (args.input_file.is_file() and
            (args.input_file.suffix == '.txt')):
        raise ValueError('Parameter[input_file] is not a .txt file.')

    args.output_file = pathlib.Path(args.output_file).resolve(strict=False)
    if not (args.output_file.suffix == '.txt'):
        raise ValueError('Parameter[output_file] is not a .txt file.')

    return args

if __name__ == '__main__':
    encoder = encoder.encoder()
    args = parse_args()

    if args.mode == 'encode':
        with open(args.input_file, 'rb') as f:
            data = f.read()
            formated_input =  ph.byte_array_to_channel_format(data)
            output = encoder.encode(formated_input)
            np.savetxt(args.output_file, output)
    if args.mode == 'decode':
        with open(args.input_file, 'rb') as f:
            data = f.read()
            formated_input =  ph.byte_array_to_channel_format(data)
            output = ph.channel_format_to_byte_array(encoder.decode(formated_input))
            np.savetxt(args.output_file, output)
    if args.mode == 'test':
        with open(args.input_file, 'rb') as i:
            with open(args.output_file, 'rb') as o:
                formated_input = ph.byte_array_to_channel_format(i.read())
                formated_output = ph.byte_array_to_channel_format(o.read())
                distance = ph.hamming_distance(formated_input,formated_output)
                if (distance == 0):
                    print("No errors!")
                else: 
                    print("There was %f errors".format(distance))
