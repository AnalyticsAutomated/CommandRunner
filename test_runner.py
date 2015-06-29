import unittest

from runner import *

# tmp_id = ''
# tmp_path = ''
# in_glob = ''
# out_glob = ''
# command = ''


class RunnerTestCase(unittest.TestCase):

    r = ''
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    in_glob = "in"
    out_glob = "out"
    cmd = "ls /tmp > [OUTPUT]"

    def setUp(self):
        self.r = runner(self.id_string, self.tmp_path,
                        self.in_glob, self.out_glob, self.cmd)

    def testInitialisation(self):
        """
            Just reasserts that initialising works
        """
        self.assertEqual(self.r.tmp_id, self.id_string)
        self.assertEqual(self.r.tmp_path, self.tmp_path)
        self.assertEqual(self.r.in_glob, self.in_glob)
        self.assertEqual(self.r.out_glob, self.out_glob)
        self.assertEqual(self.r.command, self.cmd)

    def testPathExistsWorks(self):
        """
            Check the path looks right
        """
        self.assertEqual(self.r.tmp_path, self.tmp_path)

    def testPathDoesNotExistWorks(self):
        """
            Test the non-existing path raises and exception
        """
        self.assertRaises(OSError, runner, self.id_string,
                          "/Blarghelblarghel/", self.in_glob, self.out_glob,
                          self.cmd)

    def test_translate_command_correctly_interpolate():
        pass


if __name__ == '__main__':
    unittest.main()
