import ipaddress
import unittest
import main
import requests


class BasicTest(unittest.TestCase):

    def unban(self):
        req_unban = requests.post('http://0.0.0.0:8080/unban/24')
        self.assertTrue(req_unban.status_code, 429)

        header = {'X-Forwarded-For': '123.45.67.89'}
        req = requests.get('http://0.0.0.0:8080/', headers=header)
        self.assertTrue(req.status_code, 200)

    def testGet_subnet(self):
        'assert subnet return class IPv4Address'
        self.assertIs(type(main.get_subnet('192.168.1.1', '24')), ipaddress.IPv4Address)

    def test_hadle_request(self):
        header_a = {'X-Forwarded-For': '123.45.67.89'}
        header_b = {'X-Forwarded-For': '123.45.67.1'}
        for _ in range(80):
            req_a = requests.get('http://0.0.0.0:8080/', headers=header_a)
            self.assertTrue(req_a.status_code, 200)

        for _ in range(21):
            req_b = requests.get('http://0.0.0.0:8080/', headers=header_b)
            self.assertTrue(req_b.status_code, 200)
        # unban subnet, using either ip's subnet or subnet mask
        self.unban()

    def test_unban_400(self):
        req = requests.post('http://0.0.0.0:8080/unban/24.12')
        self.assertTrue(req.status_code, 400)

    def test_req_404(self):
        req = requests.get('http://0.0.0.0:8080/Ynban/')
        self.assertTrue(req.status_code, 404)

    def test_unban_405(self):
        req = requests.get('http://0.0.0.0:8080/unban/24')
        self.assertTrue(req.status_code, 405)


if __name__ == '__main__':
    unittest.main()
