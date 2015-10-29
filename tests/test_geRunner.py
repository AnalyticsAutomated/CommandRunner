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

    # OPTIONAL
    input_string = "input.in"
    output_string = "outfile.out"
    flags = ["-lah", ]
    options = {'-a': '12', 'b': '1'}
    out_glob = ['out', ]
    input_data = {"input.in": "SOME EXAMPLE DATA"}
    std_out = ":std.out"
    interpolation_flags = ["-lah", "$INPUT", "$INPUT", "$OUTPUT"]
    interpolation_options = {'-a': '12', '$INPUT': '$OUTPUT',
                             '$OUTPUT': '$OUTPUT'}

    def setUp(self):
        self.r = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          input_string=self.input_string,
                          output_string=self.output_string,
                          flags=self.flags,
                          options=self.options,
                          std_out_string=self.std_out
                          )
        self.r2 = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command=self.cmd_simple,
                           input_data=self.input_data,
                           output_string=self.output_string,
                           flags=self.flags,
                           std_out_string=self.std_out
                           )
        self.r3 = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command=self.cmd_simple,
                           input_data=self.input_data,
                           input_string=self.input_string,
                           output_string=self.output_string,
                           flags=self.interpolation_flags,
                           options=self.interpolation_options,
                           std_out_string=self.std_out
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
        self.assertEqual(self.r.params, ['-lah', '-a 12',
                                           'b 1'])

    def test_args_list_is_correct_with_interpolation(self):
        self.r3.prepare()
        self.assertEqual(self.r3.params, ['-lah',
                                            'input.in',
                                            'input.in',
                                            'outfile.out',
                                            'input.in outfile.out',
                                            'outfile.out outfile.out',
                                            '-a 12'])

    def test_prepare_correctly_makes_directory_and_file(self):
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file1 = self.tmp_path+self.id_string+"/input.in"
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file1), True)

    def test_command_executes(self):
        self.r2.prepare()
        exit_status = self.r2.run_cmd()
        self.assertEqual(exit_status, 0)
        self.assertNotEqual(self.r2.output_data, None)

    def test_flag_and_options_interpolation_does_not_occur(self):
        self.assertEqual(self.r.command, self.cmd_simple)

    def test_space_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls ", input_data=self.input_data)
