import unittest
import os
from unittest.mock import patch

from commandRunner.geRunner import *


class geRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    r = None
    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    cmd_simple = "ls"

    # OPTIONAL
    input_string = "input.in"
    output_string = "output.out"
    flags = ["-lah", "> output.out"]
    options = {'-a': '12', 'b': '1'}
    out_glob = ['out', ]
    input_data = {"input.in": "SOME EXAMPLE DATA"}

    def setUp(self):
        self.r = geRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          input_string=self.input_string,
                          output_string=self.output_string,
                          flags=self.flags,
                          options=self.options)

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

    def test_args_list_is_correct(self):
        self.r.prepare()
        self.assertEqual(self.r.args_set, self.cmd_simple)

    def test_flag_and_options_interpolation_does_not_occur(self):
        self.assertEqual(self.r.command, self.cmd_simple)

    def test_options_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls$OPTIONS", input_data=self.input_data)

    def test_flags_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls$FLAGS", input_data=self.input_data)

    def test_input_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls$INPUT", input_data=self.input_data)

    def test_output_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls$OUTPUT", input_data=self.input_data)

    def test_space_raises_error(self):
        self.assertRaises(ValueError, geRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls ", input_data=self.input_data)
