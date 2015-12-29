# coding: utf-8

"""
Shim to allow python -m test.
This only works in python 2.7+.
"""
from __future__ import absolute_import, division, print_function, with_statement

from vanellope.test.runtests import all, main

# vanellope.test.main autodiscovery relies on 'all' being present in
# the main module, so import it here even though it is not used directly.
# The following line prevents a pyflakes warning.
all = all

main()
