#!/usr/bin/python

import os, subprocess

def use_file(filename):
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

def use_git(gitargs):
    """
    will run the git show command and return a config dictionary
    @param  gitargs = [source_path, [SHA1], [SHA2]]
    """
    working_dir = gitargs.pop(0)
    sha = [None, None]
    i = 0
    while len(gitargs):
        sha[i] = gitargs.pop(0)
        i = i+1
    # if source path without trailing slash, show error    
    # get source base path
    split_path = working_dir.split('/');
    source_base_path = "/".join(split_path[0:-2]) + '/'
    # get source dir name
    source_dir = split_path[-2]
    # get target dir
    target_dir = '../target/' + source_dir + '/'
    # run git command from working_using Popen
    command = 'git show --pretty="format:" --name-only '
    if sha[0] is not None:
        command += ' %s ' % (sha[0])
    if sha[1] is not None:
        command += ' %s ' % (sha[1])
    proc = subprocess.Popen(command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = proc.communicate()
    lines = output.split()
    return {
        "source_base_path" : source_base_path,
        "source_dir" : source_dir,
        "source_path" : working_dir,
        "target_dir" : target_dir,
        "lines" : lines,
        "ignore" : ['*.pyc', '*.class', '*~', '.svn', '.git']
        }
