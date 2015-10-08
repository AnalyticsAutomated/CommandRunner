import os
import re
import types
from subprocess import call


class commandRunner():

    tmp_id = None
    tmp_path = None
    out_globs = None
    command = None
    input_data = None
    command = None

    input_string = None

    # data = None
    # output_data = None
    # in_path = None
    # out_path = None
    # path = None
    # flags = None
    # options = None

    def __init__(self, **kwargs):
        '''
            Constructs a local job
            takes
            tmp_id = string
            tmp_path="/tmp/"
            command="ls /tmp > $OUTPUT"

            out_globs=['file',]
            input_data={filename:data_string}
            input_string="test.file"
            output_string="out.file"
            options = {flag:entry}
            flags = [strings,]
        '''

        self.__check_arguments(kwargs)

        # # if anything is passed it must be a string
        # for key, value in kwargs.items():
        #     if key is 'flags' or key is 'options'or key is 'options':
        #         continue
        #     if not isinstance(value, str) and value is not None:
        #         raise TypeError('Argument {} not a string: {}'.format(key,
        #                                                               value))
        # self.tmp_id = kwargs.pop('tmp_id', '')
        # self.in_glob = kwargs.pop('in_glob', '')
        # self.out_glob = kwargs.pop('out_glob', '')
        # self.data = kwargs.pop('input_data', '')
        # self.flags = kwargs.pop('flags', None)
        # self.options = kwargs.pop('options', None)
        # self.tmp_path = re.sub("/$", '', self.tmp_path)
        # self.path = self.tmp_path+"/"+self.tmp_id+"/"
        # if self.in_glob is not None:
        #     self.in_glob = re.sub("^\.", '', self.in_glob)
        #     self.in_path = self.path+self.tmp_id+"."+self.in_glob
        # self.out_glob = re.sub("^\.", '', self.out_glob)
        # self.out_path = self.path+self.tmp_id+"."+self.out_glob
        # self.command = self.__translate_command(kwargs.pop('command', ''))
        #
        # # ensure we have an in_glob if we have been passed data
        # if self.data is not None and self.in_glob is None:
        #     raise ValueError('in_glob missing but data provided')
        #
        # if self.tmp_path is None:
        #     raise ValueError('tmp_path missing')
        #
        # if "$INPUT" in self.command and self.in_glob is None:
        #     raise ValueError("$INPUT present in command "
        #                      "but no in_glob provided")
        # if "$FLAGS" in self.command and self.flags is None:
        #     raise ValueError("$FLAGS present in command "
        #                      "but no flags () provided")
        #
        # if "$OPTIONS" in self.command and self.options is None:
        #     raise ValueError("$OPTIONS present in command "
        #                      "but no options {{ }} provided")
        #
        # if self.command is None:
        #     raise ValueError('command is required')

    def __check_arguments(self, kwargs):

        # input_string="test.file"
        # output_string="out.file"
        # options = {flag:entry}
        # flags = (strings,)
        if os.path.isdir(kwargs['tmp_path']):
            self.tmp_path = kwargs.pop('tmp_path', '')
        else:
            raise OSError('tmp_path provided does not exist')

        if isinstance(kwargs['tmp_id'], str):
            self.tmp_id = kwargs.pop('tmp_id', '')
        else:
            raise TypeError('tmp_id must be a string')

        if isinstance(kwargs['command'], str):
            self.command = kwargs.pop('command', '')
        else:
            raise TypeError('command must be a string')

        if 'input_data' in kwargs:
            if isinstance(kwargs['input_data'], dict):
                self.input_data = kwargs.pop('input_data', '')
            else:
                raise TypeError('input_data must be a dict')

        if 'out_globs' in kwargs:
            if isinstance(kwargs['out_globs'], list):
                self.out_globs = kwargs.pop('out_globs', '')
            else:
                raise TypeError('out_globs must be array')

        if 'input_string' in kwargs:
            if isinstance(kwargs['input_string'], str):
                self.input_string = kwargs.pop('input_string', '')
            else:
                raise TypeError('input_string must be str')
            if "$INPUT" not in self.command:
                raise ValueError("input_string provided but no $INPUT in"
                                 "command string")

    def __translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        command = command.replace("$OUTPUT", self.out_path)
        if self.in_path is not None:
            command = command.replace("$INPUT", self.in_path)

        flags_str = ""
        if self.flags is not None:
            for flag in self.flags:
                flags_str += flag+" "
        flags_str = flags_str[:-1]
        command = command.replace("$FLAGS", flags_str)

        options_str = ""
        if self.options is not None:
            for key, value in sorted(self.options.items()):
                options_str += key+" "+value+" "
        options_str = options_str[:-1]
        command = command.replace("$OPTIONS", options_str)
        return(command)

    def prepare(self):
        '''
            Makes a directory and then moves the input data file there
        '''
        raise NotImplementedError

    def run_cmd(self):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        raise NotImplementedError

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        raise NotImplementedError
