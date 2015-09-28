#!/usr/bin/env python

import os
import webtemplates
import unittest
import tempfile

class WebTemp_TestCase(unittest.TestCase):

    def setUp(self):
        webtemplates.app.config['TESTING'] = True
        self.app = webtemplates.app.test_client()

    def tearDown(self):
	pass

    def test_got_rows(self):
        rv = self.app.get('/')
        assert 'C4' in rv.data

if __name__ == '__main__':
    unittest.main()
