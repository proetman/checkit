#!/usr/local/bin/python3

import unittest

from checkit_vb import main

class unittestMain(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pass(self):
        self.assertTrue(True)

    def test_simple(self):
        self.assertEqual(nthterm(1,3,1),4,msg="seq by 1, 3 times, returns 3")
        self.assertEqual(nthterm(1,100,1),102,msg="seq by 1, 100 times, returns 100")
        self.assertEqual(nthterm(1,100,2),201,msg="seq by 1, 3 times, returns 3")

# ----------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

# --- eof ---
