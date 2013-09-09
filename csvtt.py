#!/usr/bin/env python
"""CSVToTemplate

Usage:
    csvtt.py [options] <csv_data> <template>...

Options:
    -h --help               Show this screen
    -o --output=<dir>       Output directory [default: .]
    -d --dialect            CSV dialect as interpreted by python
    -b --break=<char>       Data break delimiter [default: \\v]
    -e --extension=<ext>    Extension of output files

"""

import csv
import os
from string import Template

from docopt import docopt



def main():
    """ Run the program """

    arguments = docopt(__doc__, version='CSV to Template 0.1.0')

    template_paths = [os.path.abspath(template_path) for
                      template_path in arguments['<template>']]
    data_path = os.path.abspath(arguments['<csv_data>'])
    output_dir = os.path.abspath(arguments['--output'])
    output_extension = arguments['--extension']
    breakchar = arguments['--break'].decode('string_escape')

    for template_path in template_paths:

        template_file = open(template_path, 'r')
        template = Template(template_file.read())
        output_basename = os.path.splitext(os.path.basename(template_path))[0]
        if output_extension == None:
            output_extension = os.path.splitext(template_path)[1]
        data = csv.DictReader(open(data_path, 'rU'))
        index = 0
        for row in data:

            for key in row:

                val = row[key]
                row[key] = val.replace(breakchar, '\n')

            out_file_path = os.path.join(
                    output_dir,
                    output_basename + "_" + str(index) + output_extension
             )

            out_file = open(out_file_path, 'w')
            out_file.write(template.substitute(row))
            out_file.close()
            index += 1



if __name__ == '__main__':
    main()
