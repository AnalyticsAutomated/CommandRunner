import unittest
import os
from unittest.mock import patch

from commandRunner.geRunner import *


class geRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    cmd_simple = "/usr/bin/ls"
    cmd_complex = "/usr/bin/ls $P1 $P2 $P3 $P4 $P5"
    cmd_integration "/bin/ls -lah /tmp"
    # OPTIONAL

    flags_with_options = ['-l', '-ah', '-a', 'b', '-c']
    param_values = {'-a': {'value': '12', 'spacing': True, 'switchless': True},
                    'b': {'value': '1', 'spacing': False, 'switchless': False},
                    '-c': {'value': '10', 'spacing': True, 'switchless': False}
                    }
    in_glob = ['.in', ]
    out_glob = ['.out', ]
    input_data = {"input.in": "SOME EXAMPLE DATA"}
    env_vars = {"THIS": "MANY THINGS"}
    std_out = "out.stdout"

    def setUp(self):
        self.r = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          in_globs=self.in_glob,
                          params=self.flags_with_options,
                          command=self.cmd_complex,
                          input_data=self.input_data,
                          env_vars=self.env_vars,
                          std_out_str=self.std_out
                          )
        self.r2 = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           in_globs=self.in_glob,
                           command=self.cmd_complex,
                           input_data=self.input_data,
                           params=self.flags_with_options,
                           param_values=self.param_values,
                           env_vars=self.env_vars,
                           std_out_str=self.std_out
                           )

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

    def test_args_list_is_correct_without_interpolation(self):
        self.r.prepare()
        self.assertEqual(self.r.ge_params, ['-l', '-ah', '-a', 'b', '-c'])

    def test_args_list_is_correct_with_interpolation(self):
        self.r2.prepare()
        self.assertEqual(self.r2.ge_params, ['-l',
                                             '-ah',
                                             '12',
                                             'b1',
                                             '-c 10',
                                             ])

    def test_prepare_correctly_makes_directory_and_file(self):
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file1 = self.tmp_path+self.id_string+"/input.in"
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file1), True)

    # strictly this is an integration test and should be elsewhere or at least
    # mocked here and tested in some integration tests
    def test_command_executes(self):
        self.r2.prepare()
        exit_status = self.r2.run_cmd()
        self.assertEqual(exit_status, 0)
        self.assertNotEqual(self.r2.output_data, None)

    def test_flag_and_options_interpolation_does_not_occur(self):
        self.assertEqual(self.r.command_token, self.cmd_simple)


if __name__ == '__main__':
    unittest.main()
