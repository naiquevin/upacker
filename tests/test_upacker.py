import unittest
import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "../src"),]
import methods

class MethodsTestCase(unittest.TestCase):    
    def test_find_method(self):
        command = 'pack.py --file ../manifests/kohana.txt'
        self.assertEqual(methods.find_method(command.split()), 'file')
        command = 'pack.py --git /home/vineet/javascript/mygitproject/ 3423ew 32423er'
        self.assertEqual(methods.find_method(command.split()), 'git')
        command = 'pack.py --svn /home/vineet/svnproj/'
        self.assertRaises(methods.UnsupportedMethodError, methods.find_method, command.split())        

class FileReaderTestCase(unittest.TestCase):
    def setUp(self):
        """
        manitest file location: ../manifests/opencart.txt
        with following contents
        -----------------------------------
        basepath=/home/vineet/public_html/
        basedir=opencart_v1.4.9.4

        index.php
        catalog/controller/account/account.php
        catalog/controller/account/create.php
        catalog/controller/feed/*
        catalog/model/**
        -----------------------------------
        """
        self.file = '../manifests/opencart.txt'
        self.command = 'python pack.py --file %s' % (self.file)
        self.cmd_argv = self.command.split(' ')[1:]
        self.reader = methods.FileReader(self.cmd_argv)

    def test_method_name(self):
        self.assertEqual(methods.FileReader.method, 'file')
    
    def test_init(self):
        self.assertEqual(self.reader.file, self.file)

    def test_get_property(self):
        """
        This is just a static method.
        so just provding the input params
        """
        line = 'basepath=/home/vineet/public_html/'
        self.assertEqual(methods.FileReader.get_property(line), '/home/vineet/public_html/')
        
    def test_get_lines(self):
        lines = self.reader.get_lines()
        self.assertEqual(len(lines), 8+1)
        self.assertEqual(lines[2], '')
        self.assertEqual(lines[3], 'index.php')
        self.assertEqual(lines[7], 'catalog/model/**')

    def test_get_config(self):
        config = self.reader.get_config()
        self.assertEqual(config['source_base_path'], '/home/vineet/public_html/')
        self.assertEqual(config['source_dir'], 'opencart_v1.4.9.4')
        self.assertEqual(config['source_path'], '/home/vineet/public_html/opencart_v1.4.9.4/')
        self.assertEqual(config['target_dir'], '../target/opencart_v1.4.9.4/')
        self.assertEqual(len(config['lines']), 8+1-2)
        self.assertEqual(config['ignore'], ['*.pyc', '*.class', '*~', '.svn', '.git'])

class GitReaderTestCase(unittest.TestCase):
    def setUp(self):
        hash1 = '1c5bd6ef80c37b59e752c479541b38ea9c897939'
        hash2 = '0080bcbaaca12db4a95c10bcd1c73eddf9aa4240'
        dir_path = '/home/vineet/javascript/guitarjs/'        
        self.command = 'python pack.py --git %s %s %s' % (dir_path, hash1, hash2)
        self.cmd_argv = self.command.split(' ')[1:]
        self.reader = methods.GitReader(self.cmd_argv)

    def test_init(self):
        reader = self.reader
        self.assertEqual(reader.working_dir, '/home/vineet/javascript/guitarjs/')
        self.assertEqual(len(reader.hashes), 2)

    def test_build_git_command(self):
        reader = self.reader
        # check for two hashes - 'diff'
        hashes = ['009089e3', '32f33h4']
        self.assertEqual(reader.build_git_command(hashes), 'git diff --pretty="format:" --name-only %s %s' % (hashes[0], hashes[1]))
        # check for one hash - 'show'
        hashes = ['0907d7ff']
        self.assertEqual(reader.build_git_command(hashes), 'git show --pretty="format:" --name-only %s' % (hashes[0]))

    def test_find_git_command(self):
        # check for two hashes - 'diff'
        hashes = ['009089e3', '32f33h4']
        self.assertEqual(methods.GitReader.find_git_command(hashes), 'diff')
        # check for one hash - 'show'
        hashes = ['0907d7ff']
        self.assertEqual(methods.GitReader.find_git_command(hashes), 'show')
        # check for exception raising
        hashes = []
        self.assertRaises(methods.GitHashError, methods.GitReader.find_git_command, hashes)
        hashes = ['009089e3', '32f33h4', 'fds3233']
        self.assertRaises(methods.GitHashError, methods.GitReader.find_git_command, hashes)
        
    def test_init_one_hash(self):
        hash1 = '1c5bd6ef80c37b59e752c479541b38ea9c897939'
        dir_path = '/home/vineet/javascript/guitarjs/'                
        command = 'python pack.py --git %s %s' % (dir_path, hash1)
        cmd_argv = command.split(' ')[1:]
        reader = methods.GitReader(cmd_argv)
        self.assertEqual(reader.working_dir, '/home/vineet/javascript/guitarjs/')
        self.assertEqual(len(reader.hashes), 1)


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
