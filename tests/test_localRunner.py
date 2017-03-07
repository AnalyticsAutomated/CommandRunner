import unittest
import os
from unittest.mock import patch

from commandRunner.localRunner import *

# TODO: Fixtures and actual system calls aplenty here, could all be mocked if
# I had time to fix all that. At the moment we just mock the time consuming
# calls


class localRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    r = None
    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    cmd_simple = "ls /tmp"
    cmd_complete = "ls -cd $P1 $P2 $P3 $P3 $P4 $VALUE $I1 $I1 $O1 $TMP/$ID"

    std_out_str = "out.stdout"
    # OPTIONAL
    flags = ['-l', '-ah']
    options = ['-a', 'b', '-c']
    flags_with_options = ['-l', '-ah', '-a', 'b']
    param_values = {'-a': {'value': '12', 'spacing': True, 'switchless': True},
                    'b': {'value': '1', 'spacing': False, 'switchless': False},
                    '-c': {'value': '10', 'spacing': True, 'switchless': False}
                    }
    in_glob = ['.in', ]
    out_glob = ['.out', ]
    input_data = {"input.in": "SOME EXAMPLE DATA"}
    value = "12"
    identifier = "TEST"
    def setUp(self):
        self.r = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                             out_globs=self.out_glob,
                             command=self.cmd_simple,
                             input_data=self.input_data,
                             std_out_str="outstuff")
        self.r2 = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                              out_globs=self.out_glob,
                              in_globs=self.in_glob,
                              command=self.cmd_complete,
                              input_data=self.input_data,
                              flags=self.flags,
                              options=self.options,
                              value_string=self.value,
                              identifier=self.identifier,
                              env_vars={"DIR": "/THIS/DIR/",
                                        "DIR2": "/THAT/DIR2/"})

    def tearDown(self):
        path = self.tmp_path+self.id_string
        if os.path.exists(path):
            for this_file in os.listdir(path):
                file_path = os.path.join(path, this_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except e:
                    print(e)
            os.rmdir(path)

    def test_prepare_correctly_makes_directory_and_file(self):
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file1 = self.tmp_path+self.id_string+"/input.in"
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file1), True)

    def test_prepare_correctly_makes_directory_and_multiple_files(self):
        r3 = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                         out_globs=self.out_glob, command=self.cmd_simple,
                         input_data={"input.1": "SOME EXAMPLE DATA",
                                     "input.2": "SOME EXAMPLE DATA",
                                     "input.3": "SOME EXAMPLE DATA"})
        r3.prepare()
        path = self.tmp_path+self.id_string
        file1 = self.tmp_path+self.id_string+"/input.1"
        file3 = self.tmp_path+self.id_string+"/input.3"
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file1), True)
        self.assertEqual(os.path.exists(file3), True)

    def test_prepare_without_data(self):
        r3 = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                         command=self.cmd_simple)
        r3.prepare()
        path = self.tmp_path+self.id_string
        file1 = self.tmp_path+self.id_string+"/input.in"
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file1), False)

    @patch('commandRunner.localRunner.call', return_value=0)
    def test_run(self, m):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.assertEqual(exit_status, 0)
    # TODO: more thorough testing of failure states and sensible behaviour
    # if we are not producing files

    def test_run_with_file_printing(self):
        r3 = localRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                         command="ls /tmp",
                         std_out_string=self.std_out_str)
        r3.prepare()
        exit_status = r3.run_cmd()
        self.assertEqual(exit_status, 0)
        self.assertNotEqual(r3.output_data, None)

    @patch('commandRunner.localRunner.call', return_value=1)
    def test_run_with_alternative_success_exit_status(self, m):
        self.r2.prepare()
        exit_status = self.r2.run_cmd(success_params=[1])
        self.assertEqual(exit_status, 1)

    @patch('commandRunner.localRunner.call', return_value=1)
    def test_run_with_array_of_exit_status_returning_one(self, m):
        self.r.prepare()
        exit_status = self.r.run_cmd(success_params=[0, 1])
        self.assertEqual(exit_status, 1)

    @patch('commandRunner.localRunner.call', return_value=0)
    def test_run_with_array_of_exit_status_returning_two(self, m):
        self.r.prepare()
        exit_status = self.r.run_cmd(success_params=[0, 1])
        self.assertEqual(exit_status, 0)

    def test_tidy_removes_all_files_and_dirs(self):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.r.tidy()
        self.assertEqual(os.path.exists(self.r.path), False)


if __name__ == '__main__':
    unittest.main()
