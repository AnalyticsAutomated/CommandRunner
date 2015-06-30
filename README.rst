commandRunner
=============

commandRunner is yet another package created to handle running commands,
scripts or programs on the command line. The principle class lets you run
anything locally on your machine. Later classes are targetted at Analytics
and data processing platforms such as Grid Engine and HADOOP. The class
attempts to run commands in a moderately thread safe way by requiring that
you provide with sufficient information that it can build a uniquely labelled
temp directory for all input and output files. This means that this can play
nicely with things like Celery workers.

Release 0.1
-----------

This release supports running commands on localhost.  It also uses interpolation
for the commands with the same syntax and python templates

Future
------

In the future we'll provide classes to run commands over RServe, Grid Engine,
Hadoop, Octave, and SAS Server.


Usage
-----
This is the basic usages::

    from commandRunner import *

    r = commandRunner("ID_STRING", "/tmp/", ".in", ".out", "ls /tmp > $OUTPUT",
                      "STRING OF DATA")
    r.prepare()
    exit_status = r.run_cmd()
    r.tidy()
    print(r.output_data)

__init__ initalises all the class variables needed and performs the command
string interpolation.

r.prepare() builds a temporary directory and makes any input file which is
needed. In this instance "ID_STRING", and a path where temporary files can be
placed are used to create a tempdir called /tmp/ID_STRING/. Next it takes and
string of data and makes and input file given the provided input file ending
(.in) which would be /tmp/ID_STRING/ID_STRING.in and this file would contain
"STRING OF DATA"

r.run_cmd() runs the command string provided. First anything labelled $OUTPUT
of $INPUT will be replaced with the path to the temporary files the process
will generate.  In this instance "ls /tmp > $OUTPUT" will become
"ls /tmp > /tmp/ID_STRING/ID_STRING.out". Any command will be run so this is
potentially very dangerous. The exit status of the command is returned

r.tidy() cleans up deleting any input and output files and the temporary
working directory. Any data in the output file is read in to r.output_data

Tests
-----

Run tests with:

    python test_commandRunner.py
