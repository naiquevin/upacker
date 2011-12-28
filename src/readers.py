#!/usr/bin/python

import subprocess

class FileReader(object):

    reader_type = "file"

    def __init__(self, filepath):
        self.file = filepath

    def get_lines(self):
        """
        read lines from the file and return an array of lines
        """
        f = open(self.file)
        # split may not be necessary
        return f.read().split('\n')

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
            "ignore" : ['*.pyc', '*.class', '*~', '.svn', '.git', '.gitignore']
        }

    @staticmethod
    def get_property(line):
        prop = line.split("=")
        try:
            return prop[1]
        except IndexError:
            # raise an exception here instead of sys.exit
            print 'Error: Properties specified in the manifest file not of the form key=value'
            exit()


class GitReader(object):

    reader_type = 'git'

    command_format = 'git %s --pretty="format:" --name-only'

    def __init__(self, working_dir, hash1, hash2=None):
        self.working_dir = working_dir
        self.hashes = [hash1]
        if hash2 is not None:
            self.hashes.append(hash2)

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
        command = self.git_command(self.hashes)
        lines = self.run_command(command)
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
            raise GitHashError('Unsupported number of Git hashes - (%d) - Expected - min 1, max 2' % (num_hashes))
        return cmd

    def git_command(self, hashes):
        cmd = GitReader.find_git_command(hashes)
        command = GitReader.command_format % (cmd)
        for h in hashes:
            command += ' %s' % h
        return command

    def run_command(self, command):
        proc = subprocess.Popen(command, cwd=self.working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, error) = proc.communicate()
        lines = output.split()
        return lines

class UnsupportedReaderError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr('Unsupported Reader %r' % self.value)

class TrailingSlashError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)

class GitHashError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)
