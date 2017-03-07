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
    script_simple = "print('hello')"
    script_complex = "ls $OPTIONS $FLAGS /tmp/$INPUT $OUTPUT"
    std_out_str = "out.stdout"
    # OPTIONAL
    input_string = "input.in"
    output_string = "output.out"
    flags = ['-l', '-ah']
    options = {'-a': '12', 'b': '1'}
    out_glob = ['out', ]
    input_data = {"input.in": "SOME EXAMPLE DATA"}

    def setUp(self):
        self.r = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                              out_globs=self.out_glob,
                              script=self.script_simple,
                              input_data=self.input_data,
                              std_out_str="outstuff")
        self.r2 = pythonRunner(tmp_id=self.id_string, tmp_path=self.tmp_path,
                              out_globs=self.out_glob,
                              script=self.script_complex,
                              input_data=self.input_data,
                              input_string=self.input_string,
                              output_string=self.output_string,
                              flags=self.flags,
                              options=self.options,
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


if __name__ == '__main__':
    unittest.main()
