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
    cmd_complete = "ls $OPTIONS $FLAGS /tmp/$INPUT > $OUTPUT"

    # OPTIONAL
    input_string = "input.in"
    output_string = "output.out"
    flags = ['-l', '-ah']
    options = {'-a': '12', 'b': '1'}
    out_glob = ['out', ]
    input_data = {"input.in": "INTERESTING_ID_STRING"}

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
                                options=self.options)

    # def tearDown(self):
    #     path = self.tmp_path+self.id_string
    #     file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
    #     out = self.tmp_path+self.id_string+"/"+self.id_string+self.out_glob
    #     if os.path.exists(file):
    #         os.remove(file)
    #     if os.path.exists(out):
    #         os.remove(out)
    #     if os.path.exists(path):
    #         os.rmdir(path)
    #

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

    def test_raise_if_input_string_but_not_interpolation_control(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls", input_data=self.input_data,
                          input_string="huh")

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

    def test_raise_if_output_string_but_not_interpolation_control(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls", input_data=self.input_data,
                          output_string="huh")

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

    def test_raise_if_options_but_not_interpolation_control(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls", input_data=self.input_data,
                          options={"h": "123"})

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

    def test_raise_if_flags_but_not_interpolation_control(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls", input_data=self.input_data,
                          flags=["h"])

    def test_raise_if_options_ref_but_no_options(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls $OPTIONS", input_data=self.input_data)

    def test_raise_if_flags_ref_but_no_flags(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls $FLAGS", input_data=self.input_data)

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
                           command="ls /tmp > $OUTPUT",
                           output_string="output.out")
        test_string = "ls /tmp > output.out"
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
                           out_globs=self.out_glob, command="ls $FLAGS /tmp",
                           flags=["-ls", "ah"])
        test_string = "ls -ls ah /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_options(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls $OPTIONS /tmp",
                           options={'-a': '12', 'b': '1'})
        test_string = "ls -a 12 b 1 /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_all(self):
        test_string = "ls -a 12 b 1 -l -ah /tmp/input.in > output.out"
        self.assertEqual(self.r2.command, test_string)

    # def test_prepare_correctly_makes_directory_and_file(self):
    #     self.r.prepare()
    #     path = self.tmp_path+self.id_string
    #     file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
    #     self.assertEqual(os.path.isdir(path), True)
    #     self.assertEqual(os.path.exists(file), True)
    #
    # def test_prepare_without_data(self):
    #     self.r = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
    #                          in_glob=self.in_glob, out_glob=self.out_glob,
    #                          command=self.cmd, input_data=None)
    #     self.r.prepare()
    #     path = self.tmp_path+self.id_string
    #     file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
    #     self.assertEqual(os.path.isdir(path), True)
    # #     self.assertEqual(os.path.exists(file), False)
    #
    # @patch('commandRunner.commandRunner.call', return_value=0)
    # def test_run(self, m):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd()
    #     self.assertEqual(exit_status, 0)
    # # # TODO: more thorough testing of failure states and sensible behaviour
    # if
    # # # we are not producing files
    #
    # def test_run_with_file_printing(self):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd()
    #     self.assertEqual(exit_status, 0)
    #     self.assertNotEqual(self.r.output_data, None)
    #
    # @patch('commandRunner.commandRunner.call', return_value=1)
    # def test_run_with_alternative_success_exit_status(self, m):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd(success_params=[1])
    #     self.assertEqual(exit_status, 1)
    #
    # @patch('commandRunner.commandRunner.call', return_value=1)
    # def test_run_with_array_of_exit_status_returning_one(self, m):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd(success_params=[0, 1])
    #     self.assertEqual(exit_status, 1)
    #
    # @patch('commandRunner.commandRunner.call', return_value=0)
    # def test_run_with_array_of_exit_status_returning_two(self, m):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd(success_params=[0, 1])
    #     self.assertEqual(exit_status, 0)
    #
    # def test_tidy_removes_all_files_and_dirs(self):
    #     self.r.prepare()
    #     exit_status = self.r.run_cmd()
    #     self.r.tidy()
    #     self.assertEqual(os.path.exists(self.r.path), False)
    #     self.assertEqual(os.path.exists(self.r.in_path), False)
    #     self.assertEqual(os.path.exists(self.r.out_path), False)

if __name__ == '__main__':
    unittest.main()
