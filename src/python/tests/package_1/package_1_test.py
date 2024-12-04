import unittest
from src.package_1.awesome_module import hello

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(["Hello! This is the awesome_module!"], hello)  # add assertion here


if __name__ == '__main__':
    unittest.main()
