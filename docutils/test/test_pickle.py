#! /usr/bin/env python3
# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests of document tree pickling.
"""

import unittest
import pickle
from docutils import core


class PickleTests(unittest.TestCase):

    def test_pickle(self):
        doctree = core.publish_doctree(
            source='Title\n=====\n\nparagraph\n',
            settings_overrides={'_disable_config': True})
        dill = pickle.dumps(doctree)
        reconstituted = pickle.loads(dill)
        self.assertEqual(doctree.pformat(), reconstituted.pformat())


if __name__ == '__main__':
    unittest.main()
