import unittest
import os
from unittest.mock import patch

from commandRunner.commandRunner import *

# TODO: Fixtures and actual system calls aplenty here, could all be mocked if
# I had time to fix all that. At the moment we just mock the time consuming
# calls


class commandRunnerTestCase(unittest.TestCase):

    data = "SOME EXAMPLE DATA"

    r = None
    # REQUIRED
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    cmd_simple = "ls /tmp"
    cmd_complete = "ls -cd $INPUT $OUTPUT"

    # OPTIONAL
    input_string = "input.in"
    output_string = "output.out"
    flags = ['-l', '-ah']
    options = {'-a': '12', 'b': '1'}
    out_glob = ['out', ]
    input_data = {"input.in": "INTERESTING_ID_STRING"}
    std_out_str = "out.stdout"

    def setUp(self):
        self.r = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               out_globs=self.out_glob,
                               command=self.cmd_simple,
                               input_data=self.input_data)
        self.r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                                out_globs=self.out_glob,
                                command=self.cmd_complete,
                                input_data=self.input_data,
                                input_string=self.input_string,
                                output_string=self.output_string,
                                flags=self.flags,
                                options=self.options,
                                std_out_str=self.std_out_str)

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

    def testPathExistsWorks(self):
        """
            Check the path looks right
        """
        self.assertEqual(self.r.tmp_path, "/tmp")

    def test_full_path_is_correct(self):
        self.assertEqual(self.r.path, self.tmp_path+self.id_string+"/")

    @patch('os.path.isdir', return_value=False)
    def testPathDoesNotExistWorks(self, m):
        """
            Test the non-existing path raises and exception
        """
        self.assertRaises(OSError, commandRunner, tmp_id=self.id_string,
                          tmp_path="/blerghalmcblarghel",
                          out_globs=self.out_glob,
                          command=self.cmd_simple, input_data=self.input_data)

    def test_std_out_str_is_string(self):
        self.assertEqual(self.r2.std_out_str, self.std_out_str)

    def test_std_out_str_is_not_string_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple, input_data=self.input_data,
                          std_out_str=123)

    def test_tmp_id_is_string(self):
        self.assertEqual(self.r.tmp_id, self.id_string)

    def test_tmp_id_is_not_string_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=12,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple, input_data=self.input_data)

    def test_command_is_string(self):
        self.assertEqual(self.r.command, self.cmd_simple)

    def test_command_is_not_string_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=123, input_data=self.input_data)

    def test_input_data_is_dict(self):
        self.assertEqual(self.r.input_data, self.input_data)

    def test_input_data_is_not_dict_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple, input_data=123)

    def test_will_take_blank_input_data(self):
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command=self.cmd_simple)
        self.assertEqual(r3.input_data, None)

    def test_out_globs_is_list(self):
        self.assertEqual(self.r.out_globs, self.out_glob)

    def test_out_globs_is_not_list_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=123,
                          command=self.cmd_simple, input_data=self.input_data)

    def test_will_take_blank_out_globs(self):
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r3.out_globs, None)

    def test_input_string_is_string(self):
        self.assertEqual(self.r2.input_string, self.input_string)

    def test_input_string_is_not_string_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          input_string=123)

    def test_will_take_blank_input_string(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.input_string, None)

    def test_output_string_is_string(self):
        self.assertEqual(self.r2.output_string, self.output_string)

    def test_output_string_is_not_string_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          output_string=123)

    def test_will_take_blank_output_string(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.output_string, None)

    def test_options_is_dict(self):
        self.assertEqual(self.r2.options, self.options)

    def testoptions_is_not_dict_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          options=123)

    def test_will_take_blank_options(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.options, None)

    def test_flags_is_list(self):
        self.assertEqual(self.r2.options, self.options)

    def test_flags_is_not_list_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          flags=123)

    def test_will_take_blank_flags(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.options, None)

    def test_raise_if_input_ref_but_no_intput_string(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls $INPUT", input_data=self.input_data)

    def test_raise_if_output_ref_but_no_output_string(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls $OUTPUT", input_data=self.input_data)

    def test_translate_command_correctly_interpolate_output(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command="ls /tmp $OUTPUT",
                           output_string="output.out")
        test_string = "ls /tmp output.out"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_input(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls /tmp $INPUT",
                           input_string="input.in")
        test_string = "ls /tmp input.in"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_flags(self):
        """
        test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls /tmp",
                           flags=["-ls", "ah"])
        test_string = "ls -ls ah /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_options(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls /tmp",
                           options={'-a': '12', 'b': '1'})
        test_string = "ls -a 12 b 1 /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_all(self):
        test_string = "ls -l -ah -a 12 b 1 -cd input.in output.out > out.stdout"
        self.assertEqual(self.r2.command, test_string)

if __name__ == '__main__':
    unittest.main()
