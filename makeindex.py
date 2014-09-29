#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
makeindex
"""
import sys
import urllib

import jinja2
import path as Path


def filter_ipynb(path):
    """
    select files for inclusion in index
    """
    # exclude .ipynb_checkpoints directories
    if '.ipynb_checkpoints' in path:
        return False
    return True


def find_notebooks(path, pattern='*.ipynb',
                   base_url=None, filterfn=filter_ipynb):
    _base_url = None
    if base_url:
        _, _url = urllib.splittype(base_url)
        _base_url = base_url and Path.path(
            u'/'.join(('http://nbviewer.ipython.org', _url.lstrip('/'))))
    _path = Path.path(path)
    for ipynb in _path.walk(pattern=pattern):
        if filterfn(ipynb):
            html = None
            _html = ipynb.splitext()[0] + '.html'
            if Path.path(_html).exists():
                html = _html
            yield {
                'ipynb': ipynb,
                'html': html,
                'nbviewer': base_url and _base_url / ipynb}


def makeindex(template, path='.',
              pattern='*.ipynb',
              base_url=None,
              filterfn=filter_ipynb):
    """
    Generate an HTML index for a set of ipython notebooks

    Templates:
     * index.jinja  -- HTML index
     * readme.jinja -- README.md index
    """
    context = {
        'notebooks': list(
            find_notebooks(path, base_url=base_url, filterfn=filterfn)),
    }
    templatedir = Path.path(__file__).abspath().dirname() / 'templates'
    loader = jinja2.FileSystemLoader(templatedir)
    env = jinja2.Environment()  # autoescape=True
    tmpl = loader.load(env, template)
    return tmpl.render(context)


import unittest


class Test_makeindex(unittest.TestCase):

    def test_makeindex_html(self):
        output = makeindex('index.jinja', path='.')
        self.assertIn('IPython notebooks', output)
        self.assertIn('<li>', output)
        self.assertIn('<a href=".', output)

    def test_makeindex_readme_md(self):
        output = makeindex('readme.jinja', path='.')
        self.assertIn('IPython notebooks', output)
        self.assertIn('*', output)
        self.assertIn('<a href=".', output)


def main(*args):
    import optparse
    import logging

    prs = optparse.OptionParser(usage="%prog: [args]")

    prs.add_option('--base-url',
                   dest='base_url',
                   action='store')

    prs.add_option('--html',
                   dest='html',
                   action='store_true')
    prs.add_option('--readme',
                   dest='readme',
                   action='store_true')

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)
    prs.add_option('-t', '--test',
                   dest='run_tests',
                   action='store_true',)

    args = args and list(args) or sys.argv[1:]
    (opts, args) = prs.parse_args(args)

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    if opts.run_tests:
        sys.argv = [sys.argv[0]] + args
        sys.exit(unittest.main())

    if opts.html:
        output = makeindex("index.jinja", path='.', base_url=opts.base_url)
        print(output)

    if opts.readme:
        output = makeindex("readme.jinja", path='.', base_url=opts.base_url)
        print(output)

    return 0

if __name__ == "__main__":
    sys.exit(main())
