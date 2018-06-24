#!/usr/bin/env python

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Input raw file')
    parser.add_argument('outfile', nargs='?', help='Output processed file. Empty for stdout')
    parser.add_argument('--template', default='header.tpl', help='Template filename')
    parser.add_argument('--bpr', type=int, default=16, help='Bytes per row')

    return parser.parse_args()

def main():
    args = parse_args()

    f = open(args.infile, 'rb')
    data = [hex(b) for b in f.read()]
    f.close()

    tf = open(args.template, 'r')
    template = tf.read()
    tf.close()

    block = [data[offset*args.bpr:offset*args.bpr + args.bpr] for offset in range(len(data) // args.bpr)]

    context = {'samples': '\n'.join([','.join(s) for s in block])}
    output = template % context

    if args.outfile is None:
        print(output)
    else:
        fout = open(args.outfile, 'w')
        fout.write(output)
        fout.close()

if __name__ == '__main__':
    main()

