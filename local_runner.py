class localRunner:
    tmp_id = ''
    tmp_path = ''
    in_glob = ''
    out_glob = ''
    command =  = ''

    def __init__(self, tmp_id, tmp_path, in_glob, out_glob, cmd):
        ''' Constructs a local job '''
        self.tmp_id = tmp_id
        self.tmp_path = tmp_path
        self.in_glob = in_glob
        self.out_glob = out_glob
        self.command = _translate_command(cmd, tmp_path, tmp_id, in_glob, out_glob)

    def _translated_command(command, path, id, input, output):
        '''
            takes the command string and substitutes the relevant files names
        '''
        #sub [INPUT] in command string for id+"."+input
        #sub [OUTPUT] in command string for id+"."+output
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

    def _find_complete():
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
