commandRunner
=============

commandRunner is yet another package created to handle running commands,
scripts or programs on the command line. Targetted at thread safe execution
for Celery. The simplest class lets you run anything locally on your machine.
Other classes are targeted at Analytics and data processing platforms such as
Grid Engine (and eventually HADOOP). The class attempts to run commands in a
moderately threadsafe way by requiring that you provide it with sufficient
information that it can build a uniquely labeled temporary directory for all
input and output files. This means that this can play nicely with things like
Celery workers.

Release 0.7.0
-------------

This release supports running commands on local unix shell and DRMAA compliant grid
engine installs (ogs, soge and univa). We can also run strings of python
code.  Commands are built/interpolated via some simple rule described bellow.

Future
------

In the future we'll provide classes to run commands over RServe,
Hadoop, Octave, and SAS Server.

Usage
-----
This is the basic usage for running a binary using the local unix shell::

    from commandRunner.localRunner import *

    r = localRunner(tmp_id="ID_STRING", tmp_path=,/tmp/", out_glob=['file', ],
                    command="ls /tmp", input_data={DATA_DICT})
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

__init__ initalises all the class variables needed and performs the command
string interpolation which allow you to parameterise the command.

Interpolation rules work the following way. The command string is split in to
tokens. The tokens are serched for specific control flags the define inputs,
output, paths and command parameters. Take the following call::

    r = localRunner(tmp_id="ID_STRING",
                    tmp_path="/tmp/",
                    out_glob=['.file', ],
                    params=["-a","-l", "b"]
                    param_values={'b': {'value': 'this',
                                   'spacing': True,
                                   'switchless': False},
                             }
                    command="ls $P1 $P2 $P$ /tmp",
                    input_data={DATA_DICT},
                    str_out_str="file.stdout",
                    identifier="string"
                    env_vars={"str":"str"},)

This effectively builds the following command::

      ls -a -l b this /tmp > file.stdout

Command string interpolation accepts a range of control sequences which begin
with $.

If you provide a list of strings via the in_glob function variable these
will be made availabe in the command string using $I[int]. tmp_id string and
each sequential entry in the in_glob list are concatenated. For tmp_id="this"
and in_glob=[".in", ".thing", ] two strings are created this.in and this.thing
and they can be refered to in the command string as $I1 and $I2.

A near identical interpolation is carried out for the out_glob list providing
$O[int]. With tmp_id="this" and out_glob=['.file', ] string this.file will be
created and can be refered to in the command string as $O1.

Command line parameters are more subtle. These will be available as $P[int]
where each integer refers to a successive entry in the params list. If
param_values is not provided then the values in params will be interpolated
as the appear in the params list. If params_values is provided then more
sophisticated control of the param interpolation can be achieved. Providing
a value (12) means that a param entry ("b") will be interpolated as "b 12".
Setting spacing to false suppresses the space, "b12" and setting switchless to
True suppresses the param name "12".

We also provide a couple of convenience strings $TMP, $ID and $VALUE. There
will interpolate the contents of tmp_path, tmp_id and value_string respectively

Next it takes input_data. This is a dict of {Filename:Data_string} values.
Iterating over, it writes the data to a file given the values in temp_path and
temp_id. So given the following dict and the values above::

    { "test.file" : "THIS IS MY STRING OF DATA"}

would result in a file with the path /tmp/ID_STRING/test.file

env_vars is a dict of key:value strings which is used to set the unix
environment variables for the running command.

Note that only tmp_id, tmp_path and command are required. Omitting
input_data or out_glob assumes that there are respectively no input files to
write or output files to gather and interpolations for $I[int], $O[int] and
$P[int] will not reference anything.

The line r.run_cmd(success_params=[0]) runs the command string provided.

Once complete if out_globs have been provided and the files were output then
the contents of those files can be found in the dict r.output_data. which has
the same {Filename:Data_string} form as the input_data dict::

{ "output.file" : "THIS IS MY PROCESSED DATA"}

r.tidy() cleans up deleting any input and output files and the temporary
working directory. Any data in the output file is available in to r.output_data

Grid Engine Quirks
------------------

geRunner uses python DRMAA to submit jobs. A consequence of this that a command
string is not constructed in quite the same way. The first portion of the
command string is split off as a command. Subsequence portions are tokenised
and added to a params array to be passed to DRMAA

The Options dict is flattened to a key:value list. You can include or omit as
many of those as you'd like options as you like. Any instance of the string
$I[int] and $O[int] in final args array will be interpolated as usual

If std_out_string is provided it will be used as
a file where the Grid Engine thread STDOUT will be captured::

    from commandRunner.geRunner import *

    r = geRunner(tmp_id="ID_STRING", tmp_path="/tmp/", out_glob=['.file'],
                 command="ls -lah", input_data={"File.txt": "DATA"},
                 params = ["-file"]
                 param_values = {"-file": {'value': '$O1',
                                   'spacing': True,
                                   'switchless': False},
                                 },
                 std_out_string="std.out")
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

Although DRMAA functions differently you can think of this as effectively
run the following command (after following the interpolation rules)::

   ls -file out.file -lah > std.out

Tests
-----

Best to run these 1 suite at a time, geRunner tests will fail if you do not
have Grid Engine installed, DRMAA_LIBRARY_PATH set and SGE_ROOT set, for example::

    export DRMAA_LIBRARY_PATH=/opt/ogs_src/GE2011.11/lib/linux-x64/libdrmaa.so
    export SGE_ROOT=/opt/ogs_src/GE2011.11/

Run tests with::

    python setup.py test -s tests/test_commandRunner.py
    python setup.py test -s tests/test_localRunner.py
    python setup.py test -s tests/test_geRunner.py
    python setup.py test -s tests/test_pythonRunner.py

TODO
----

1. Implement rserveRunner for running commands in r
2. Implement hadoopRunner for running command on Hadoop
3. Implement sasRunner for a SAS backend
4. Implement octaveRunner for Octave backend
5. matlab? mathematica?
