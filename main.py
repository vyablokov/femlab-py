#!/usr/bin/env pypy3

import yaml
import argparse
import sys
import time
from femstatement import FemStatement, FemCubicStatement
import linear_elems

def howlong(func):
    def tmp():
        startTime = time.time()
        func()
        print('Pure calculation time: %.3f s' % (time.time() - startTime))
    return tmp

@howlong
def main():
    parser = argparse.ArgumentParser(description='Input options for %(prog)s', prog='femlab-py',
                                     usage='{0:s} -c CONFIG'.format(sys.argv[0]))
    parser.add_argument('-c', '--config', help='specify path to configuration file')
    parser.add_argument('-o', '--out', nargs='?', help='specify path to output file')

    options = parser.parse_args(sys.argv[1:])
    fileName = options.config
    settingsFile = open(fileName, 'r')
    loadedSettings = yaml.load(settingsFile)
    settingsFile.close()

    statement = FemStatement(loadedSettings)


    results = linear_elems.driver(statement)
    # for i in range(0, statement.nodesNum()):
    #     print(results[i])

    file = open(options.out, 'w')
    for raw in range(0, statement.nodesNum()):
        file.write('{0:4f}\t\t{1:4f}\n'.format(results[raw][0],
                                               results[raw][1]))
    file.close()

if __name__ == '__main__':
    main()
