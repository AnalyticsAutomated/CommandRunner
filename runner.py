import os


class runner:
    tmp_id = ''
    tmp_path = ''
    in_glob = ''
    out_glob = ''
    command = ''

    def __init__(self, tmp_id, tmp_path, in_glob, out_glob, cmd):
        ''' Constructs a local job '''

        if os.path.isdir(tmp_path):
            self.tmp_path = tmp_path
        else:
            raise OSError

        self.tmp_id = tmp_id
        self.in_glob = in_glob
        self.out_glob = out_glob
        self.command = self.__translate_command(cmd)

    def __translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # sub [INPUT] in command string for id+"."+input
        # sub [OUTPUT] in command string for id+"."+output
        return(command)

    def prepare():
        '''
            Makes a directory and then moves the input data file there
        '''
        pass

    def run_cmd():
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        pass

    def __find_complete():
        '''
            read the exit status
        '''
        pass

    def move_results():
        '''
            put the command output where you've been told
        '''
        pass

    def tidy():
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        pass
