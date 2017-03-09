import unittest
import os
from unittest.mock import patch

from commandRunner.rRunner import *

# TODO: Fixtures and actual system calls aplenty here, could all be mocked if
# I had time to fix all that. At the moment we just mock the time consuming
# calls


class rRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    r = None
    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp"
    path = tmp_path+"/"+id_string+"/"
    script_simple = "print('hello')"

    std_out_str = "out.stdout"
    # OPTIONAL
    flags = ['-l', '-ah']
    options = {'-a': '12', 'b': '1'}
    in_glob = ['.in', ]
    out_glob = ['.out', ]
    flags_with_options = ['-l', '-ah', '-a', 'b']
    param_values = {'-a': {'value': '12', 'spacing': True, 'switchless': True},
                    'b': {'value': '1', 'spacing': False, 'switchless': False},
                    '-c': {'value': '10', 'spacing': True, 'switchless': False}
                    }
    input_data = {"input.in": "SOME EXAMPLE DATA",
                  "input.this": "MORE DATA"}

    def setUp(self):
        kwarg_set = {'tmp_id': self.id_string,
                     'tmp_path': self.tmp_path,
                     'std_out_str': "outstuff", }
        self.r = rRunner(script=self.script_simple, **kwarg_set)
        kwarg_set["in_globs"] = self.in_glob
        kwarg_set["input_data"] = self.input_data
        self.r2 = rRunner(script=self.script_simple, **kwarg_set)
        kwarg_set["in_globs"] = self.in_glob+["this"]
        self.r3 = rRunner(script=self.script_simple, **kwarg_set)
        kwarg_set["in_globs"] = []
        kwarg_set["out_globs"] = self.out_glob
        self.r4 = rRunner(script=self.script_simple, **kwarg_set)
        kwarg_set["out_globs"] = []
        kwarg_set["params"] = self.flags_with_options
        kwarg_set["param_values"] = self.param_values
        self.r5 = rRunner(script=self.script_simple, **kwarg_set)
        kwarg_set["in_globs"] = self.in_glob
        kwarg_set["input_data"] = self.input_data
        kwarg_set["out_globs"] = self.out_glob
        self.r6 = rRunner(script=self.script_simple, **kwarg_set)
        self.r7 = rRunner(script="print('hu)", **kwarg_set)
        self.r8 = rRunner(script="write('hello', stderr())", **kwarg_set)
        self.r9 = rRunner(script="cat('hello', file=O1)", **kwarg_set)
        self.r10 = rRunner(script="data<-readLines(I1)\nprint(data)", **kwarg_set)

    # def tearDown(self):
    #     path = self.tmp_path+self.id_string
    #     if os.path.exists(path):
    #         for this_file in os.listdir(path):
    #             file_path = os.path.join(path, this_file)
    #             try:
    #                 if os.path.isfile(file_path):
    #                     os.unlink(file_path)
    #             except e:
    #                 print(e)
    #         os.rmdir(path)

    def test_prepare_with_without_files_or_params(self):
        self.r.prepare()
        self.assertEqual(self.r.script_header,
                         "setwd('"+self.path+"')"
                         "\n")

    def test_prepare_with_just_infiles(self):
        self.r2.prepare()
        self.assertEqual(self.r2.script_header,
                         "setwd('"+self.path+"')\n"
                         "I1 <- file('input.in', 'r')\n")

    def test_prepare_with_multiple_infiles(self):
        self.r3.prepare()
        self.assertEqual(self.r3.script_header,
                         "setwd('"+self.path+"')\n"
                         "I1 <- file('input.in', 'r')\n"
                         "I2 <- file('input.this', 'r')\n"
                         )

    def test_prepare_with_outfiles(self):
        self.r4.prepare()
        self.assertEqual(self.r4.script_header,
                         "setwd('"+self.path+"')\n"
                         "O1 <- file('INTERESTING_ID_STRING.out', 'w')\n")

    def test_prepare_with_params(self):
        self.r5.prepare()
        self.assertEqual(self.r5.script_header,
                         "setwd('"+self.path+"')\n"
                         "P1 <- TRUE\nP2 <- TRUE\n"
                         "P3 <- list()\n"
                         "P3[['-a']] <- '12'\n"
                         "P4 <- list()\n"
                         "P4[['b']] <- '1'\n")

    def test_script_looks_sane_after_prepare(self):
        self.r6.prepare()
        self.assertEqual(self.r6.script_header,
                         "setwd('"+self.path+"')\n"
                         "I1 <- file('input.in', 'r')\n"
                         "O1 <- file('INTERESTING_ID_STRING.out', 'w')\n"
                         "P1 <- TRUE\nP2 <- TRUE\n"
                         "P3 <- list()\n"
                         "P3[['-a']] <- '12'\n"
                         "P4 <- list()\n"
                         "P4[['b']] <- '1'\n")
        self.assertEqual(self.r6.script, "print('hello')")
        self.assertEqual(self.r6.script_footer, "close(I1)\nclose(O1)\n")

    # integration tests from here
    def test_user_script_can_raise_and_write_to_stderr_file(self):
        self.r7.prepare()
        self.r7.run_cmd()
        self.assertTrue("unexpected INCOMPLETE_STRING" in
                        self.r7.output_data[self.id_string+".stderr"])

    def test_user_script_can_write_to_stderr_file(self):
        self.r8.prepare()
        self.r8.run_cmd()
        self.assertTrue("RRuntimeWarning: hello" in
                        self.r8.output_data[self.id_string+".stderr"])

    def test_user_script_will_write_to_stdout_file(self):
        self.r6.prepare()
        self.r6.run_cmd()
        self.assertEqual(self.r6.output_data["outstuff"], "[1]\n "
                                                          "\"hello\"\n\n\n")

    def test_user_script_will_does_not_gather_data_if_output_blank(self):
        self.r6.prepare()
        self.r6.run_cmd()
        self.assertFalse(self.id_string+self.out_glob[0] in
                         self.r6.output_data)

    def test_user_script_will_write_to_output_file(self):
        self.r9.prepare()
        self.r9.run_cmd()
        self.assertEqual(self.r9.output_data[self.id_string+self.out_glob[0]],
                         b"hello")

    def test_user_script_will_read_input_and_echo_stdout(self):
        self.r10.prepare()
        self.r10.run_cmd()
        self.assertEqual(self.r10.output_data["outstuff"],
                         "[1]\n "
                         "\"SOME EXAMPLE DATA\"\n\n\n")

if __name__ == '__main__':
    unittest.main()
