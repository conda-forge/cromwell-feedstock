#!/usr/bin/env python3
#
# Wrapper script for invoking the jar.
#
# This script is written for use with the Conda package manager and is ported
# from a bash script that does the same thing, adapting the style in
# the peptide-shaker wrapper
# (https://github.com/bioconda/bioconda-recipes/blob/master/recipes/peptide-shaker/peptide-shaker.py)

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Expected name of the JAR file.
JAR_NAME = 'womtool.jar'
PKG_NAME = 'cromwell'

# Default options passed to the `java` executable.
DEFAULT_JVM_MEM_OPTS = ('-Xms512m', '-Xmx1g')


def jvm_opts(argv, default_mem_opts=DEFAULT_JVM_MEM_OPTS
             ) -> Tuple[List[str], List[str], List[str]]:
    """Constructs a list of Java arguments based on our argument list.


    The argument list passed in argv must not include the script name.
    The return value is a 3-tuple lists of strings of the form:
        (memory_options, prop_options, passthrough_options)

    """
    mem_opts, prop_opts, pass_args = [], [], []

    for arg in argv:
        if arg.startswith('-D') or arg.startswith('-XX'):
            prop_opts.append(arg)
        elif arg.startswith('-Xm'):
            mem_opts.append(arg)
        else:
            pass_args.append(arg)

    if mem_opts == [] and os.getenv('_JAVA_OPTIONS') is None:
        mem_opts = list(default_mem_opts)

    return mem_opts, prop_opts, pass_args


def main():
    script = Path(sys.argv[0])
    prefix = script.parent.parent      # Script is in prefix/bin/script.
    jar_path = Path(prefix, "share", PKG_NAME, JAR_NAME)

    mem_opts, prop_opts, pass_args = jvm_opts(sys.argv[1:])

    if pass_args != [] and pass_args[0].startswith('org'):
        jar_arg = '-cp'
    else:
        jar_arg = '-jar'

    java_args: List[str] = (["java"] + mem_opts + prop_opts +
                            [jar_arg] + [str(jar_path)] + pass_args)
    sys.exit(subprocess.call(java_args))


if __name__ == "__main__":
    main()
