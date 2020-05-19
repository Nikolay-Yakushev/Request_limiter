import ipaddress
import unittest

import main


class BasicTest(unittest.TestCase):

    # вообще можно проверить, послав запрос??
    def testGet_subnet(self):
        'assert subnet return class IPv4Address'
        self.assertIs(type(main.get_subnet('192.168.1.1', '24')), ipaddress.IPv4Address)


if __name__ == '__main__':
    unittest.main()
