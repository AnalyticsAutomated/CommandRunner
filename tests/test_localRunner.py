
import unittest
import os
from unittest.mock import patch

from commandRunner.localRunner import *

# TODO: Fixtures and actual system calls aplenty here, could all be mocked if
# I had time to fix all that. At the moment we just mock the time consuming
# calls


class localRunnerTestCase(unittest.TestCase):

    r = None
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    in_glob = ".in"
    out_glob = ".out"
    cmd = "ls /tmp > $OUTPUT"
    data = "SOME EXAMPLE DATA"

    def setUp(self):
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             in_glob=self.in_glob, out_glob=self.out_glob,
                             command=self.cmd, input_data=self.data)

    def tearDown(self):
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        out = self.tmp_path+self.id_string+"/"+self.id_string+self.out_glob
        if os.path.exists(file):
            os.remove(file)
        if os.path.exists(out):
            os.remove(out)
        if os.path.exists(path):
            os.rmdir(path)

    def testInitialisation(self):
        """
            Just reasserts that initialising works
        """
        self.assertEqual(self.r.tmp_id, self.id_string)
        self.assertEqual(self.r.in_glob, "in")
        self.assertEqual(self.r.out_glob, "out")

    def testPathExistsWorks(self):
        """
            Check the path looks right
        """
        self.assertEqual(self.r.tmp_path, "/tmp")

    @patch('os.path.isdir', return_value=False)
    def testPathDoesNotExistWorks(self, m):
        """
            Test the non-existing path raises and exception
        """
        self.assertRaises(OSError, localRunner, tmp_id=self.id_string,
                          tmp_path="/blerghalmcblarghel",
                          in_glob=self.in_glob, out_glob=self.out_glob,
                          command=self.cmd, input_data=self.data)

    def testRaisesErrorifDataProvidedButNoinGlob(self):
        """
            Test the non-existing path raises and exception
        """
        self.assertRaises(ValueError, localRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path, in_glob=None,
                          out_glob=self.out_glob, command=self.cmd,
                          input_data=self.data)

    def testHappyWithNoinglobAndNoData(self):
        """
            Test the non-existing path raises and exception
        """
        r = localRunner(tmp_id=self.id_string,
                        tmp_path=self.tmp_path, in_glob=None,
                        out_glob=self.out_glob, command=self.cmd,
                        input_data=None)

    def test_translate_command_correctly_interpolate_output(self):
        """
            test __translated_command works as expected
        """
        test_string = "ls /tmp > " \
                      "/tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_translate_command_correctly_interpolate_input(self):
        """
            test __translated_command works as expected
        """
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             in_glob=self.in_glob, out_glob=self.out_glob,
                             command="ls /tmp > $INPUT", input_data=self.data)
        test_string = "ls /tmp > " \
                      "/tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.in"
        self.assertEqual(self.r.command, test_string)

    def test_rejectedIfINPUTbutNoInGlob(self):
        """
            Rejects if $INPUT in command but no inglob provided
        """
        self.assertRaises(ValueError, localRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path, in_glob=None,
                          out_glob=self.out_glob, command="ls /tmp > $INPUT "
                                                          "$OUTPUT",
                          input_data=self.data)

    def test_translate_command_correctly_interpolate_both(self):
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             in_glob=self.in_glob, out_glob=self.out_glob,
                             command="ls /tmp > $INPUT $OUTPUT",
                             input_data=self.data)
        test_string = "ls /tmp > " \
                      "/tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.in " \
                      "/tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_translate_command_correctly_handles_globs_without_periods(self):
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             in_glob="in", out_glob="out",
                             command=self.cmd, input_data=self.data)

        test_string = "ls /tmp > " \
                      "/tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_prepare_correctly_makes_directory_and_file(self):
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file), True)

    def test_prepare_without_data(self):
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             in_glob=self.in_glob, out_glob=self.out_glob,
                             command=self.cmd, input_data=None)
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        self.assertEqual(os.path.isdir(path), True)
    #     self.assertEqual(os.path.exists(file), False)

    @patch('commandRunner.localRunner.call', return_value=0)
    def test_run(self, m):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.assertEqual(exit_status, 0)
    # # TODO: more thorough testing of failure states and sensible behaviour if
    # # we are not producing files

    def test_run_with_file_printing(self):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.assertEqual(exit_status, 0)
        self.assertNotEqual(self.r.output_data, None)

    @patch('commandRunner.localRunner.call', return_value=1)
    def test_run_with_alternative_success_exit_status(self, m):
        self.r.prepare()
        exit_status = self.r.run_cmd(success_param=1)
        self.assertEqual(exit_status, 1)

    def test_tidy_removes_all_files_and_dirs(self):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.r.tidy()
        self.assertEqual(os.path.exists(self.r.path), False)
        self.assertEqual(os.path.exists(self.r.in_path), False)
        self.assertEqual(os.path.exists(self.r.out_path), False)


if __name__ == '__main__':
    unittest.main()
