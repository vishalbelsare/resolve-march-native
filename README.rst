.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. image:: https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml/badge.svg
   :target: https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml
   :alt: Run the test suite


About
=====

``resolve-march-native`` is a small command line tool to resolve
``-march=native`` into explicit GCC flags.


Example
=======

::

    $ resolve-march-native --vertical
    -march=bonnell
    -mno-cx16
    --param l1-cache-line-size=64
    --param l1-cache-size=24

Usage
=====

::

    $ COLUMNS=80 resolve-march-native --help
    usage: resolve-march-native [-h] [--debug] [--gcc COMMAND] [--vertical]
                                [--keep-identical-mtune] [--keep-mno-flags]
                                [--add-recommended] [--version]

    options:
      -h, --help            show this help message and exit
      --debug               enable debugging (default: disabled)
      --gcc COMMAND         gcc command (default: gcc)
      --vertical            produce vertical output (default: horizontal output)
      --keep-identical-mtune
                            keep implied -mtune=... despite architecture identical
                            to -march=... (default: stripped away)
      --keep-mno-flags      keep -mno-* parameters (default: (superfluous ones)
                            stripped away)
      --add-recommended, -a
                            add recommended flags (default: not added)
      --version             show program's version number and exit

    resolve-march-native is software libre licensed under GPL v2 or later,
    written by Sebastian Pipping.  Please report bugs to
    https://github.com/hartwork/resolve-march-native/issues.  Thanks!
