#!/usr/bin/env python
import argparse
import glob
import loguru
import os

logger = loguru.logger


def combine_files(root):
    g = glob.glob(f'{root}_*.json')

    output_file_name = f'./{root}.json'
    with open(output_file_name, 'w') as output_file:
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


def clean_file(filename):
    output_lines = []

    with open(filename, "r") as file:
        lines = file.readlines()
        lines[0] = lines[0][1:]
        lines[-1] = lines[-1][:-1]
        for line in lines:
            if line not in output_lines:
                output_lines.append(line)

        diff = len(lines) - len(output_lines)

    with open(f'clean_{filename}', "w") as file:
        logger.info(f'Removed {diff} duplicates, saving...')
        file.write("[")
        for i, line in enumerate(output_lines):
            file.write(line)
        file.write("]")



def main():
    parser = argparse.ArgumentParser(
        description='Combine multiple JSON files for training')
    parser.add_argument('--combine', metavar='FILE_ROOT', type=str, nargs=1,
                        help='The string at the start of each JSON file')
    parser.add_argument('--clean', metavar='FILENAME', type=str, nargs=1,
                        help='JSON file to be cleaned')


    args = parser.parse_args()
    combine = args.combine
    clean = args.clean
    if combine is not None:
        combine_files(combine[0])
    elif clean is not None:
        clean_file(clean[0])


if __name__ == "__main__":
    main()

