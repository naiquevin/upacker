#!/usr/bin/python2.6

import os
from sys import argv
from shutil import copy, copytree, rmtree, ignore_patterns

# the upload packer

def parse_lines(filename):
    """
    parse lines from the file and return 
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


class Packer(object):
    """
    Take a config object as input, loops through the 
    lines in the input file and make the correct file operations 
    for copying all the files mentioned in the file to the 
    target location.
    """

    def __init__(self, config):
        self.config = config
        # endings for all files to be ignored derived from ignore list
        self.ignore_file_endings = [ignore[ignore.find('*')+1:] for ignore in self.config["ignore"]]
        self.__del_existing()
        self.__start()
        
    def __del_existing(self):
        """
        delete the target dir if it exists already
        """
        if os.path.exists(self.config["target_dir"]):
            rmtree(self.config["target_dir"])
    
    def __start(self):        
        """
        loop through all the non empty lines
        """
        lines = self.config["lines"]
        for line in lines:
            if line == '':
                continue
            self.__pack(line)

    def __pack(self, line):
        """
        parse each line and handle various cases which are - 
        * (all files inside a dir),
        ** (entire dir tree below a dir)
        filename (a file)
        """
        struct = line.split('/')
        # print struct    
        if len(struct) > 0:
            # get last element which will be the filename
            filename = struct.pop()
            struct.append('') # append empty string for a trailing slash
            dir_path = "/".join(struct) 
            if filename == '*':
                self.__pack_dir(dir_path)
            elif filename == '**':
                self.__pack_dir_recursive(dir_path)
            else :
                self.__pack_file(dir_path, filename)
    

    def __pack_file(self, dir_path, filename):
        """
        copy the file from the source location 
        to the destination after making sure 
        the parent dir exists
        """
        # get the path of the file        
        file_path = self.__get_file_path(dir_path, filename)
        # create the directory in target if doesn't exist already
        target_dir_path = self.__mk_target_dir(dir_path)
        # copy the file
        copy(file_path, target_dir_path)

    def __pack_dir(self, dir_path):
        """
        handle the case '*'
        this will copy all files inside the specified dir
        to the destination dir after making sure the destination 
        dir exists. Only files will be copied, sub-dirs will be skipped
        """
        full_dir_path = self.__get_src_path(dir_path)
        # create the directory in target if doesn't exist already
        target_dir_path = self.__mk_target_dir(dir_path)
        children = os.listdir(full_dir_path)
        for child in children:
            full_path = os.path.join(full_dir_path, child)        
            # the continue condition here can be replaced with a 
            # list comprehension expression
            if os.path.isdir(full_path):
                continue
            elif not self.__is_ignored(child):
                # copy the file if its not to be ignored
                copy(full_path, target_dir_path)
                
    def __pack_dir_recursive(self, dir_path):
        """
        handle case "**"
        All files and sub dirs under this dir 
        will be recursively copied to the destination
        """
        full_dir_path = self.__get_src_path(dir_path)
        target_dir_path  = self.__get_target_path(dir_path)
        copytree(full_dir_path, target_dir_path, ignore=ignore_patterns(*tuple(self.config["ignore"])))

    def __get_src_path(self, dir_path):
        """
        gets the absolute path of a source dir
        from config
        """
        return self.config["source_path"] + dir_path

    def __get_file_path(self, dir_path, filename):
        """
        gets the absolute path of the file inside the 
        source dir which is to be copied
        """
        return self. __get_src_path(dir_path) + filename

    def __get_target_path(self, dir_path):
        """
        gets the absolute path of the dir inside the target dir
        """
        return self.config["target_dir"] + dir_path

    def __mk_target_dir(self, dir_path):
        """
        make a directory inside the target if it doesn't exist already
        and return the absolute path of it in either case
        """
        target_dir_path = self.__get_target_path(dir_path)        
        if not os.path.exists(target_dir_path):
            os.makedirs(target_dir_path)  
        return target_dir_path

    def __is_ignored(self, filename):
        """
        checks if the file should be ignored while copying 
        all files from inside a dir.
        """
        for end in self.ignore_file_endings:
            if filename.endswith(end):
                return True
        return False

    def output(self):
        """
        create a message to be shown to the user, after the process
        is successfully completed
        """
        return {
            "target_path" : self.config["target_dir"]
            }


def show_usage():
    """
    will show the usage if no argument is found
    """
    line = '-'
    line_length = 70
    print line * line_length
    readme = open('../README.txt')
    print readme.read()
    print line * line_length  
    
        
# test run
if __name__ == "__main__":
    
    try:
        script, filename = argv
    except ValueError:
        show_usage()
        exit(1)

    config = parse_lines(filename)
    p = Packer(config) 
    output = p.output()
    print "Project files packed to %s" % (output["target_path"])
