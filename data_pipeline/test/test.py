import unittest
from rename import process_name_price_with


class MyTestCase(unittest.TestCase):
    def test_rename(self):
        res = process_name_price_with('../data')
        print(res)

        self.assertEqual(res['inshape'], (10000, 2))
        self.assertEqual(res['outshape'], (10000, 4))  


if __name__ == '__main__':
    unittest.main()
