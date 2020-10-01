#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
productseq
"""


def productseq():
    """mainfunc

    Arguments:
         (str): ...

    Keyword Arguments:
         (str): ...

    Returns:
        str: ...

    Yields:
        str: ...

    Raises:
        Exception: ...
    """
    pass


import unittest


class Test_productseq(unittest.TestCase):

    def setUp(self):
        pass

    def test_productseq(self):
        pass

    def tearDown(self):
        pass


def main(argv=None):
    """
    Main function

    Keyword Arguments:
        argv (list): commandline arguments (e.g. sys.argv[1:])
    Returns:
        int:
    """
    import logging
    import optparse

    prs = optparse.OptionParser(usage="%prog : args")

    prs.add_option('-v', '--verbose',
                    dest='verbose',
                    action='store_true',)
    prs.add_option('-q', '--quiet',
                    dest='quiet',
                    action='store_true',)
    prs.add_option('-t', '--test',
                    dest='run_tests',
                    action='store_true',)


    (opts, args) = prs.parse_args(args=argv)
    loglevel = logging.INFO
    if opts.verbose:
        loglevel = logging.DEBUG
    elif opts.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)
    log = logging.getLogger()
    argv = list(argv) if argv else []
    log.debug('argv: %r', argv)
    log.debug('opts: %r', opts)
    log.debug('args: %r', args)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        return unittest.main()

    EX_OK = 0
    output = productseq()
    return EX_OK


if __name__ == "__main__":
    import sys
    sys.exit(main(argv=sys.argv[1:]))
