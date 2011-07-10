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
        self.command = 'pack.py --file %s' % (self.file)
        self.cmd_argv = self.command.split(' ')
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
        print config
        self.assertEqual(config['source_base_path'], '/home/vineet/public_html/')
        self.assertEqual(config['source_dir'], 'opencart_v1.4.9.4')
        self.assertEqual(config['source_path'], '/home/vineet/public_html/opencart_v1.4.9.4/')
        self.assertEqual(config['target_dir'], '../target/opencart_v1.4.9.4/')
        self.assertEqual(len(config['lines']), 8+1-2)
        self.assertEqual(config['ignore'], ['*.pyc', '*.class', '*~', '.svn', '.git'])
        

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
