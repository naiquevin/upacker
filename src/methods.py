#!/usr/bin/python

import os, subprocess

def find_method(cmd_argv):
    if cmd_argv[1] == '--file':
        method = 'file'
    elif cmd_argv[1] == '--git':
        method = 'git'
    else:
        raise UnsupportedMethodError('method not supported')
    return method

class FileReader(object):

    method = "file"

    def __init__(self, cmd_argv):
        self.argv = cmd_argv
        self.file = self.argv[2]        
        
    def get_config(self):
        """
        parse lines from a file and return 
        a config dictionary
        """
        lines = self.get_lines()
        source_base_path = FileReader.get_property(lines[0])
        if not source_base_path.endswith('/'):
            raise TrailingSlashError('Trailing slash missing in one or more paths specified')            
        source_dir = FileReader.get_property(lines[1])
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

    def get_lines(self):
        f = open(self.file)
        return f.read().split('\n')

    @staticmethod
    def get_property(line):
        prop = line.split("=")
        try:
            return prop[1]
        except IndexError:
            print 'Error: Properties specified in the manifest file not of the form key=value'
            exit()


class GitReader(object):
    
    method = 'git'

    command_format = 'git %s --pretty="format:" --name-only'

    def __init__(self, cmd_argv):
        gitargs = cmd_argv[2:]        
        self.working_dir = gitargs.pop(0)
        self.hashes = []
        while len(gitargs):
            self.hashes.append(gitargs.pop(0))

    def get_config(self):
        # if source path without trailing slash, show error    
        # get source base path
        split_path = self.working_dir.split('/');
        source_base_path = "/".join(split_path[0:-2]) + '/'
        # get source dir name
        source_dir = split_path[-2]
        # get target dir
        target_dir = '../target/' + source_dir + '/'
        # run git command from working_using Popen
        self.command = self.build_git_command(self.hashes)
        lines = self._get_command_op()
        return {
            "source_base_path" : source_base_path,
            "source_dir" : source_dir,
            "source_path" : self.working_dir,
            "target_dir" : target_dir,
            "lines" : lines,
            "ignore" : ['*.pyc', '*.class', '*~', '.svn', '.git']
            }

    @staticmethod
    def find_git_command(hashes):
        num_hashes = len(hashes)
        if num_hashes == 2:
            cmd = 'diff'
        elif num_hashes == 1:
            cmd = 'show'
        else:
            raise GitHashError('Unsupported number(%d) of Git hashes' % (num_hashes))
        return cmd

    def build_git_command(self, hashes):
        cmd = GitReader.find_git_command(hashes)
        command = GitReader.command_format % (cmd)        
        for h in hashes:
            command += ' %s' % h
        return command

    def _get_command_op(self):
        proc = subprocess.Popen(self.command, cwd=self.working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, error) = proc.communicate()
        lines = output.split()
        return lines

class UnsupportedMethodError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)        

class TrailingSlashError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)

class GitHashError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)

