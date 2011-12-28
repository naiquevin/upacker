#!/usr/bin/env python

from sys import argv
from readers import FileReader, GitReader, UnsupportedReaderError
from pack import Packer

def show_usage():
    """
    will show the usage if no argument is found
    """
    line = '-'
    line_length = 70
    sep = line * line_length
    print sep
    print 'Upacker Usage:'
    print sep
    readme = open('../docs/usage.txt')
    print readme.read()
    print sep

def get_reader(cmd_argv):
    """
    function to get the correct reader object as per the command
    """
    if cmd_argv[1] == '--file':
        reader = FileReader(cmd_argv[2])
    elif cmd_argv[1] == '--git':
        args = cmd_argv[2:]
        wd = args.pop(0)
        hash1 = args.pop(0)
        try:
            hash2 = args.pop(0)
        except IndexError:
            hash2 = None
        reader = GitReader(wd, hash1, hash2)
    else:
        raise UnsupportedReaderError(cmd_argv[1])
    return reader

if __name__ == "__main__":
    valid = True
    try:
        reader = get_reader(argv)
    except UnsupportedReaderError:
        valid = False
    except IndexError: # if argv[1] is not found
        valid = False
    if not valid:
        show_usage()
        exit(1)
    config = reader.get_config()
    p = Packer(config)
    output = p.output()
    print "Project files packed to %s" % (output["target_path"])
