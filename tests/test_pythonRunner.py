import unittest
import os
from unittest.mock import patch

from commandRunner.pythonRunner import *

# TODO: Fixtures and actual system calls aplenty here, could all be mocked if
# I had time to fix all that. At the moment we just mock the time consuming
# calls


class pythonRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    r = None
    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    script_simple = "print('hello')"
    script_raise = "raise ValueError"
    script_stderr = "import sys\nprint('hello', file=sys.stderr)"
    script_print_output = "O1.write('hello')"
    script_print_input = "print(I1.read())\n"

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
                     'in_globs': self.in_glob,
                     'out_globs': self.out_glob,
                     'input_data': self.input_data,
                     'std_out_str': "outstuff",
                     'params': self.flags_with_options,
                     'param_values': self.param_values}
        self.r = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                              script=self.script_simple,
                              std_out_str="outstuff")
        self.r2 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               script=self.script_simple,
                               in_globs=self.in_glob,
                               input_data=self.input_data,
                               std_out_str="outstuff")
        self.r3 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               script=self.script_simple,
                               in_globs=['.in', '.this'],
                               input_data=self.input_data,
                               std_out_str="outstuff")
        self.r4 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               script=self.script_simple,
                               out_globs=self.out_glob,
                               input_data=self.input_data,
                               std_out_str="outstuff")
        self.r5 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               script=self.script_simple,
                               input_data=self.input_data,
                               std_out_str="outstuff",
                               params=self.flags_with_options,
                               param_values=self.param_values)
        self.r6 = pythonRunner(script=self.script_simple, **kwarg_set)
        self.r7 = pythonRunner(script=self.script_raise, **kwarg_set)
        self.r8 = pythonRunner(script=self.script_stderr, **kwarg_set)
        self.r9 = pythonRunner(script=self.script_print_output, **kwarg_set)
        self.r10 = pythonRunner(script=self.script_print_input,
                                env_vars={"DIR": "/THIS/DIR/",
                                "DIR2": "/THAT/DIR2/"}, **kwarg_set)
        self.r11 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                                script=self.script_simple,
                                std_out_str="outstuff",
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

    def test_prepare_with_without_files_or_params(self):
        self.r.prepare()
        self.assertEqual(self.r.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')"
                         "\n")

    def test_prepare_with_withenv_vars(self):
        self.r11.prepare()
        self.assertEqual(self.r11.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "os.environ['DIR'] = '/THIS/DIR/'\n"
                         "os.environ['DIR2'] = '/THAT/DIR2/'"
                         "\n")

    def test_prepare_with_just_infiles(self):
        self.r2.prepare()
        self.assertEqual(self.r2.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "I1 = open('input.in', 'r')\n")

    def test_prepare_with_multiple_infiles(self):
        self.r3.prepare()
        self.assertEqual(self.r3.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "I1 = open('input.in', 'r')\n"
                         "I2 = open('input.this', 'r')\n")

    def test_prepare_with_outfiles(self):
        self.r4.prepare()
        self.assertEqual(self.r4.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "O1 = open('INTERESTING_ID_STRING.out', 'w')\n")

    def test_prepare_with_params(self):
        self.r5.prepare()
        self.assertEqual(self.r5.script_header,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "P1 = True\nP2 = True\nP3 = {'-a': '12'}\n"
                         "P4 = {'b': '1'}\n")

    def tests_script_looks_sane_after_prepare(self):
        self.r6.prepare()
        self.assertEqual(self.r6.script,
                         "import os\nos.chdir('/tmp/INTERESTING_ID_STRING/')\n"
                         "I1 = open('input.in', 'r')\n"
                         "O1 = open('INTERESTING_ID_STRING.out', 'w')\n"
                         "P1 = True\nP2 = True\nP3 = {'-a': '12'}\n"
                         "P4 = {'b': '1'}\nprint('hello')\n"
                         "I1.close()\nO1.close()\n")

    def test_syntax_error_raises_expection_in_prepare(self):
        self.r7 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               script="print('hi)",
                               in_globs=self.in_glob,
                               out_globs=self.out_glob,
                               input_data=self.input_data,
                               std_out_str="outstuff",
                               params=self.flags_with_options,
                               param_values=self.param_values)
        self.assertRaises(SyntaxError, self.r7.prepare)

    def test_user_script_will_write_to_output_file(self):
        self.r9.prepare()
        self.r9.run_cmd()
        self.assertEqual(self.r9.output_data[self.id_string+self.out_glob[0]],
                         b"hello")

    def test_user_script_will_does_not_gather_data_if_output_blank(self):
        self.r6.prepare()
        self.r6.run_cmd()
        self.assertFalse(self.id_string+self.out_glob[0] in
                         self.r6.output_data)

    def test_user_script_will_read_input_and_echo_stdout(self):
        self.r10.prepare()
        self.r10.run_cmd()
        self.assertEqual(self.r10.output_data["outstuff"],
                         "SOME EXAMPLE DATA\n")

    def test_user_script_will_write_to_stdout_file(self):
        self.r6.prepare()
        self.r6.run_cmd()
        self.assertEqual(self.r6.output_data["outstuff"], "hello\n")

    def test_user_script_can_write_to_stderr_file(self):
        self.r8.prepare()
        self.r8.run_cmd()
        self.assertEqual(self.r8.output_data[self.id_string+".stderr"],
                         "hello\n")

    def test_user_script_can_raise_and_write_to_stderr_file(self):
        self.r7.prepare()
        self.r7.run_cmd()
        self.assertTrue("ValueError" in
                        self.r7.output_data[self.id_string+".stderr"])

if __name__ == '__main__':
    unittest.main()
