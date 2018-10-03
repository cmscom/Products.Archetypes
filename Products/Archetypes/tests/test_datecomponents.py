from Products.Archetypes.tests.attestcase import ATTestCase
from Testing import ZopeTestCase as ztc
import unittest
import doctest


def test_suite():
    optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite('browser/datecomponents.txt',
                             package='Products.Archetypes',
                             test_class=ATTestCase,
                             optionflags=optionflags),
    ])
