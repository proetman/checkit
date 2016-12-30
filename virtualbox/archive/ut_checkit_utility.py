#!/usr/local/bin/python3

import unittest

from checkit_utility import *

class unittestinit_log_filename(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pass(self):
        self.assertTrue(True)

    def test_simple(self):
        now = time.strftime("%Y%m%d_%H%M%S")
        self.assertEqual(init_log_filename('prog', 'target_name', now), 'prog_target_name_' + now + '.log', msg="Failed on parameter concat")
        self.assertEqual(init_log_filename('prog', 'target name', now), 'prog_targetname_' + now + '.log', msg="Failed on removing internal spaces")
        self.assertEqual(init_log_filename(' prog ', 'target name', now), 'prog_targetname_' + now + '.log', msg="Failed on trimming spaces")

# ----------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

# --- eof ---
