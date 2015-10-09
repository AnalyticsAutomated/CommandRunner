commandRunner
=============

commandRunner is yet another package created to handle running commands,
scripts or programs on the command line. The simplest class lets you run
anything locally on your machine. Later classes are targetted at Analytics
and data processing platforms such as Grid Engine and HADOOP. The class
attempts to run commands in a moderately thread safe way by requiring that
you provide with sufficient information that it can build a uniquely labelled
temp directory for all input and output files. This means that this can play
nicely with things like Celery workers.

Release 0.3
-----------

This release supports running commands on localhost and DRMAA compliant grid
engine installs (ogs, soge and univa). It also uses interpolation
for the commands with the same syntax as python templates

Future
------

In the future we'll provide classes to run commands over RServe,
Hadoop, Octave, and SAS Server.


Usage
-----
This is the basic usage::

    from commandRunner import *

    r = localRunner(tmp_id="ID_STRING", tmp_path=,/tmp/", out_glob=['file'],
                    command="ls /tmp > $OUTPUT", input_data={DATA_DICT}
                    input_string="test.file", output_string="out.file")
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

__init__ initalises all the class variables needed and performs the command
string interpolation.

r.prepare() builds a temporary directory and makes any input file which is
needed. In this instance "ID_STRING", and a path where temporary files can be
placed are used to create a tempdir called /tmp/ID_STRING/.

Next it takes input_data. This is a dict of {Filename:Data_string} values.
Iterating over, it writes the data to each named file in the tempdir. So the
following dict::

    { "test.file" : "THIS IS MY STRING OF DATA"}


would result in a file with the path /tmp/ID_STRING/test.file

out_glob is an array of file suffixes which we want to gather up when the
command completes.

Not that only tmp_id, tmp_path and command are required. Omitting
input_data or out_glob assumes that there are respectively no input files to
write or output files to gather.

The line r.run_cmd(success_params=[0]) runs the command string provided.

The command string supports some limited interpolation. First anything
labeled $INPUT or $OUTPUT will be replaced with the input_string and
output_string. $OPTIONS will interpolate a dictionary of switches and values.
$FLAGS will interpolate an array of flags.

In the given example "ls /tmp > $OUTPUT" will become "ls /tmp > out.file".
Additionally We can also provide an array of unix exits statuses we consider to
be successful exists, default is [0]. Any command will be run so this is
potentially very dangerous. The exit status of the command is returned.

r.tidy() cleans up deleting any input and output files and the temporary
working directory. Any data in the output file is read in to r.output_data

Grid Engine Quirks
------------------

geRunner uses python DRMAA to submit jobs. A consequence of this is that $INPUT,
$OUTPUT, $FLAGS and $OPTIONS are NOT supported. These are concatenated in to an
array of arguments that are passed to the command by the DRMAA layer in this
order:

    [$INPUT, $FLAGS, $OPTIONS, $OUTPUT]

The Options dict is flattened to a key:value list. You can include or omit as
many of those as you'd like.

Tests
-----

Best to run these 1 suite at a time, geRunner tests will fail if you do not
have ogs installed and DRMAA_LIBRARY_PATH set

Run tests with:

    python setup.py test -s tests/test_commandRunner.py
    python setup.py test -s tests/test_localRunner.py
    python setup.py test -s tests/test_geRunner.py

TODO
----

1. Support multiple input files and multiple output files
2. Implement rserveRunner for running commands in r
3. Implement geRunner for running commands on Grid Engine
4. Implement hadoopRunner for running command on Hadoop
5. Refactor commandRunner to abstract base class
6. Move commandRunner tests out of localRunner tests
7. Implement sasRunner for a SAS backend
8. Implement octaveRunner for Octave backend
9. matlab? mathematica?
