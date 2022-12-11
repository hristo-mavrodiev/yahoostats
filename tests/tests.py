import unittest
from yahoostats.evaluator import combine_stats


class TestMethods(unittest.TestCase):
    def test_zero(self):
        print("Sample test to test the testings :)")
        self.assertEqual(":)", ":)")

    def test_evaluator(self):
        """
        Test of merging requests with selenium data
        """
        stock_list = ['GOOGL', 'INTC', 'NOSETETS']
        self.assertTrue(combine_stats(stock_list) is not None)


if __name__ == '__main__':
    unittest.main()
