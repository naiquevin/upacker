import unittest
import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "../src"),]
from readers import FileReader, GitReader, GitHashError
import cli

class ReaderTestCase(unittest.TestCase):
    def test_get_reader(self):
        command = 'pack.py --file ../manifests/kohana.txt'
        reader = cli.get_reader(command.split())
        self.assertIsInstance(reader, cli.FileReader)
        command = 'pack.py --git /home/vineet/javascript/mygitproject/ 3423ew 32423er'
        reader = cli.get_reader(command.split())
        self.assertIsInstance(reader, cli.GitReader)
        command = 'pack.py --svn /home/vineet/svnproj/'
        self.assertRaises(cli.UnsupportedReaderError, cli.get_reader, command.split())

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
        self.reader = FileReader(self.file)

    def test_reader_type(self):
        self.assertEqual(FileReader.reader_type, 'file')

    def test_init(self):
        self.assertEqual(self.reader.file, self.file)

    def test_get_property(self):
        """
        This is just a static method.
        so just providing the input params
        """
        line = 'basepath=/home/vineet/public_html/'
        self.assertEqual(FileReader.get_property(line), '/home/vineet/public_html/')

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

class GitReaderTestCase(unittest.TestCase):
    def setUp(self):
        hash1 = '1c5bd6ef80c37b59e752c479541b38ea9c897939'
        hash2 = '0080bcbaaca12db4a95c10bcd1c73eddf9aa4240'
        working_dir = '/home/vineet/javascript/guitarjs/'
        self.reader = GitReader(working_dir, hash1, hash2)

    def test_init(self):
        self.assertEqual(self.reader.working_dir, '/home/vineet/javascript/guitarjs/')
        self.assertEqual(len(self.reader.hashes), 2)

    def test_git_command(self):
        reader = self.reader
        # check for two hashes - 'diff'
        hashes = ['009089e3', '32f33h4']
        self.assertEqual(reader.git_command(hashes), 'git diff --pretty="format:" --name-only %s %s' % (hashes[0], hashes[1]))
        # check for one hash - 'show'
        hashes = ['0907d7ff']
        self.assertEqual(reader.git_command(hashes), 'git show --pretty="format:" --name-only %s' % (hashes[0]))

    def test_find_git_command(self):
        # check for two hashes - 'diff'
        hashes = ['009089e3', '32f33h4']
        self.assertEqual(GitReader.find_git_command(hashes), 'diff')
        # check for one hash - 'show'
        hashes = ['0907d7ff']
        self.assertEqual(GitReader.find_git_command(hashes), 'show')
        # check for exception raising
        hashes = []
        self.assertRaises(GitHashError, GitReader.find_git_command, hashes)
        hashes = ['009089e3', '32f33h4', 'fds3233']
        self.assertRaises(GitHashError, GitReader.find_git_command, hashes)

    def test_init_single_hash(self):
        working_dir = '/home/vineet/javascript/guitarjs/'
        hash1 = '1c5bd6ef80c37b59e752c479541b38ea9c897939'
        reader = GitReader(working_dir, hash1)
        self.assertEqual(reader.working_dir, '/home/vineet/javascript/guitarjs/')
        self.assertEqual(len(reader.hashes), 1)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
