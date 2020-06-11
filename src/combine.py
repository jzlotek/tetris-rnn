#!/usr/bin/env python
import argparse
import glob
import loguru
import os

logger = loguru.logger


def combine_files(root):
    g = glob.glob(f'{root}*.json')

    output_file_name = f'./{root}.json', 'w'
    with open(output_file_name) as output_file:
        output_file.write("[")

        for i, input_file_name in enumerate(g):
            with open(input_file_name, 'r') as input_file:
                lines = input_file.readlines()
                lines[0] = lines[0][1:]
                lines[-1] = lines[-1][:-1]

                output_file.write(''.join(lines))
                if i != len(g)-1:
                    output_file.write(",\n")
            logger.info(f'Wrote {input_file_name}...')

        output_file.write("]")

    for input_file_name in g:
        logger.info(f'Deleting {input_file_name}...')
        os.remove(input_file_name)

    logger.info(f'Aggregated {len(g)} datasets into {output_file_name}')


def main():
    parser = argparse.ArgumentParser(
        description='Combine multiple JSON files for training')
    parser.add_argument('file_root', metavar='FILE_ROOT', type=str, nargs=1,
                        help='The string at the start of each JSON file')

    args = parser.parse_args()
    combine_files(args.file_root[0])


if __name__ == "__main__":
    main()

