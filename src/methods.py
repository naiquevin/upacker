#!/usr/bin/python

import os

def get_config_from_file(filename):
    """
    parse lines from a file and return 
    a config dictionary
    """
    f = open(filename)

    lines = f.read().split('\n') 

    source_base_path = lines[0].split('=')[1]
    source_dir = lines[1].split('=')[1]
    source_path = source_base_path + source_dir + '/'
    target_dir = '../target/' + source_dir + '/'
    
    return {
        "source_base_path" : source_base_path,
        "source_dir" : source_dir,
        "source_path" : source_path,
        "target_dir" : target_dir,
        "lines" : lines[2:],
        "ignore" : ['*.pyc', '*.class', '*~', '.svn', '.git']
        }

def get_config_from_git(gitargs):
    """
    will run the git show command and return a config dictionary
    @param  gitargs = (source_path, SHA1, SHA2(optional))
    """
    # if source path without trailing slash, show error
    
    # get source base path
    split_path = source_path.split('/');
    source_base_path = split_path[0:-2]

    # get source dir name
    source_dir = split_path[-2]

    # get target dir
    target_dir = '../target/' + source_dir + '/'    

    lines = []

    return {
        "source_base_path" : source_base_path,
        "source_dir" : source_dir,
        "source_path" : source_path,
        "target_dir" : target_dir,
        "lines" : lines[2:],
        "ignore" : ['*.pyc', '*.class', '*~', '.svn', '.git']
        }
