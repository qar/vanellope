#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, division, print_function, with_statement

import sys
from tornado.testing import unittest

TEST_MODULES = [
    'vanellope.test.database_test',
    'vanellope.test.pages_test',
    'vanellope.test.apiv1_test'
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

class TornadoTextTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(TornadoTextTestRunner, self).run(test)
        if result.skipped:
            skip_reasons = set(reason for (test, reason) in result.skipped)
            self.stream.write(textwrap.fill(
                "Some tests were skipped because: %s" %
                ", ".join(sorted(skip_reasons))))
            self.stream.write("\n")
        return result

def main():
    import tornado.testing

    kwargs = {}
    kwargs['testRunner'] = TornadoTextTestRunner

    try:
        tornado.testing.main(**kwargs)
    finally:
        sys.exit(1)


if __name__ == '__main__':
    main()
