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
    cmd_complete = "ls -cd $P1 $P2 $P3 $P3 $P4 $VALUE $I1 $I1 $O1 $TMP/$ID"

    # OPTIONAL
    flags = ['-l', '-ah']
    options = ['-a', 'b', '-c']
    flags_with_options = ['-l', '-ah', '-a', 'b']
    param_values = {'-a': {'value': '12', 'spacing': True, 'switchless': True},
                    'b': {'value': '1', 'spacing': False, 'switchless': False},
                    '-c': {'value': '10', 'spacing': True, 'switchless': False}}
    in_glob = ['.in', ]
    out_glob = ['.out', ]
    identifier = "TEST"
    input_data = {"input.in": "INTERESTING_ID_STRING"}
    std_out_str = "out.stdout"
    env_vars = {"DIR": "/THIS/DIR/", "DIR2": "/THAT/DIR2/"}

    def setUp(self):
        self.r = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               out_globs=self.out_glob,
                               command=self.cmd_simple,
                               input_data=self.input_data)
        self.r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                                in_globs=self.in_glob,
                                out_globs=self.out_glob,
                                command=self.cmd_complete,
                                input_data=self.input_data,
                                identifier=self.identifier,
                                params=self.flags_with_options,
                                param_values=self.param_values,
                                std_out_str=self.std_out_str,
                                env_vars=self.env_vars,
                                value_string="path")

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
        self.assertEqual(r3.out_globs, [])

    def test_in_globs_is_list(self):
        self.assertEqual(self.r.in_globs, [])

    def test_in_globs_is_not_list_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          in_globs=123,
                          command=self.cmd_simple, input_data=self.input_data)

    def test_will_take_blank_out_globs(self):
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r3.in_globs, [])


    def test_env_vars_is_dict(self):
        self.assertEqual(self.r2.env_vars, self.env_vars)

    def test_env_vars_is_not_dict_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          env_vars=[1, 2, 3])

    def test_env_vars_raises_if_key_is_not_string(self):
        """
            test __translated_command works as expected
        """
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          env_vars={1: "this", "huh": "that"})

    def test_env_vars_raises_if_value_is_not_string(self):
        """
            test __translated_command works as expected
        """
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_complete,
                          input_data=self.input_data,
                          env_vars={"Well": 1, "huh": "that"})


    def test_params_is_list(self):
        self.assertEqual(self.r2.params, self.flags_with_options)

    def test_params_is_not_list_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          params=123)

    def test_will_take_blank_params(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.params, [])

    def test_raise_if_value_ref_but_no_value_string(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command="ls $VALUE", input_data=self.input_data)

    def test_param_values_is_dict(self):
        self.assertEqual(self.r2.param_values, self.param_values)

    def test_param_values_is_not_dict_raises_type_error(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values=[])

    def test_will_take_blank_param_values(self):
        r2 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           command=self.cmd_simple)
        self.assertEqual(r2.param_values, {})

    def test_raise_if_param_values_does_not_contain_dict_values(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values={'a': []})

    def test_raise_if_param_values_is_missing_keys(self):
        self.assertRaises(ValueError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values={'a': {'things': '123'}})

    def test_raise_if_param_values_value_is_not_str(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values={'a': {'value': 123,
                                              'switchless': True,
                                              'spacing': True}})

    def test_raise_if_param_values_switchless_is_not_boolean(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values={'a': {'value': '123',
                                              'switchless': "True",
                                              'spacing': True}})

    def test_raise_if_param_values_spacing_is_not_boolean(self):
        self.assertRaises(TypeError, commandRunner, tmp_id=self.id_string,
                          tmp_path=self.tmp_path,
                          out_globs=self.out_glob,
                          command=self.cmd_simple,
                          input_data=self.input_data,
                          param_values={'a': {'value': '123',
                                              'switchless': True,
                                              'spacing': "True"}})


    def test_translate_command_correctly_interpolate_output(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command="ls /tmp $O1")
        test_string = "ls /tmp INTERESTING_ID_STRING.out"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_multiple_output(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=['.out', '.other'],
                           command="ls /tmp $O1 $O2")
        test_string = "ls /tmp INTERESTING_ID_STRING.out"

    def test_translate_command_correctly_interpolate_input(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           in_globs=self.in_glob,
                           out_globs=self.out_glob, command="ls /tmp $I1",)
        test_string = "ls /tmp INTERESTING_ID_STRING.in"
        self.assertEqual(r3.command, test_string)

        def test_translate_command_correctly_interpolate_multiple_input(self):
            """
                test __translated_command works as expected
            """
            r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                               in_globs=['.in', '.this'],
                               out_globs=self.out_glob,
                               command="ls /tmp $I1 $I2",)
            test_string = "ls /tmp INTERESTING_ID_STRING.in " \
                          "INTERESTING_ID_STRING.this"
            self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_tmp(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls /tmp $TMP")
        test_string = "ls /tmp /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_value_string(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls /tmp $VALUE",
                           value_string="things")
        test_string = "ls /tmp things"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_flag_params(self):
        """
        test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob, command="ls $P1 $P2 /tmp",
                           params=self.flags)
        test_string = "ls -l -ah /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_option_params(self):
        """
        test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command="ls $P1 $P2 $P3 /tmp",
                           params=self.options, param_values=self.param_values)
        test_string = "ls 12 b1 -c 10 /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_option__and_flags(self):
        """
        test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command="ls $P1 $P2 $P3 $P4 /tmp",
                           params=self.flags_with_options,
                           param_values=self.param_values)
        test_string = "ls -l -ah 12 b1 /tmp"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_appends_stdout_redirect(self):
        """
            test __translated_command works as expected
        """
        r3 = commandRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                           out_globs=self.out_glob,
                           command="ls $P1 $P2 $P3 $P4 /tmp",
                           params=self.flags_with_options,
                           param_values=self.param_values,
                           std_out_str="str.stdout")
        test_string = "ls -l -ah 12 b1 /tmp > str.stdout"
        self.assertEqual(r3.command, test_string)

    def test_translate_command_correctly_interpolate_all(self):
        test_string = "ls -cd -l -ah 12 12 b1 path INTERESTING_ID_STRING.in " \
                      "INTERESTING_ID_STRING.in INTERESTING_ID_STRING.out " \
                      "/tmp/TEST > out.stdout"
        self.assertEqual(self.r2.command, test_string)


if __name__ == '__main__':
    unittest.main()
