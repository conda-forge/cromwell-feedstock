#!/usr/bin/env python3
#
# Wrapper script for invoking the jar.
#
# This script is written for use with the Conda package manager and is ported
# from a bash script that does the same thing, adapting the style in
# the peptide-shaker wrapper
# (https://github.com/bioconda/bioconda-recipes/blob/master/recipes/peptide-shaker/peptide-shaker.py)

import subprocess
import sys
import os

from pathlib import Path

# Expected name of the JAR file.
from typing import List

JAR_NAME = 'cromwell.jar'
PKG_NAME = 'cromwell'

# Default options passed to the `java` executable.
DEFAULT_JVM_MEM_OPTS = ('-Xms512m', '-Xmx1g')


def jar_dir_from_bin_file(in_path: Path) -> Path:
    """Returns the path to the JAR file"""
    full_path = in_path.resolve()  # x/x/bin/my_script
    # go to x/x/share/PKG_name
    jar_path = full_path.parent.parent / "share" / PKG_NAME
    return jar_path


def java_executable() -> Path:
    """Returns the name of the Java executable."""
    java_home = os.getenv('JAVA_HOME')
    java_bin = Path('bin', 'java')
    env_prefix = jar_dir_from_bin_file(Path(sys.argv[0])).parent.parent

    if java_home and os.access(str(Path(java_home, java_bin)), os.X_OK):
        return Path(java_home, java_bin)
    else:
        # Use Java installed with Anaconda to ensure correct version
        return env_prefix / 'bin' / 'java'


def jvm_opts(argv, default_mem_opts=DEFAULT_JVM_MEM_OPTS):
    """Constructs a list of Java arguments based on our argument list.


    The argument list passed in argv must not include the script name.
    The return value is a 3-tuple lists of strings of the form:
        (memory_options, prop_options, passthrough_options)

    """
    mem_opts, prop_opts, pass_args = [], [], []

    for arg in argv:
        if arg.startswith('-D') or arg.startswith('-XX'):
            opts_list = prop_opts
        elif arg.startswith('-Xm'):
            opts_list = mem_opts
        else:
            opts_list = pass_args
        opts_list.append(arg)

    if mem_opts == [] and os.getenv('_JAVA_OPTIONS') is None:
        mem_opts = list(default_mem_opts)

    return mem_opts, prop_opts, pass_args


def main():
    java = java_executable()
    jar_dir = jar_dir_from_bin_file(Path(sys.argv[0]))
    (mem_opts, prop_opts, pass_args) = jvm_opts(sys.argv[1:])

    if pass_args != [] and pass_args[0].startswith('org'):
        jar_arg = '-cp'
    else:
        jar_arg = '-jar'

    jar_path = jar_dir / JAR_NAME
    java_args: List[str] = ([java] + mem_opts + prop_opts +
                            [jar_arg] + [str(jar_path)] + pass_args)
    sys.exit(subprocess.call(java_args))


if __name__ == "__main__":
    main()
