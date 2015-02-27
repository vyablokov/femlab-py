#!/usr/bin/env pypy3

import yaml
import argparse
import sys
from femstatement import FemStatement, FemCubicStatement

def main():
    parser = argparse.ArgumentParser(description='Input options for %(prog)s', prog='femlab-py',
                                     usage='{0:s} -c CONFIG'.format(sys.argv[0]))
    parser.add_argument('-c', '--config', help='specify path to configuration file')

    options = parser.parse_args(sys.argv[1:])
    fileName = options.config
    settingsFile = open(fileName, 'r')
    loadedSettings = yaml.load(settingsFile)
    settingsFile.close()

    statement = FemCubicStatement(loadedSettings)

if __name__ == '__main__':
    main()
