import unittest

from src.utils.url_validator_v2 import URLValidator


class TestURLValidator(unittest.TestCase):
    def setUp(self):
        self.validator = URLValidator()

    def test_valid_urls(self):
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "ftp://example.com",
            "http://localhost",
            "http://192.168.0.1",
            "http://[2001:db8::1]",
            "http://example.co.uk",
            "http://sub.domain.example.com",
            "https://example.com/path/to/resource?query=param#fragment",
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(self.validator.is_valid_url(url))

    def test_invalid_urls(self):
        invalid_urls = [
            "htp://example.com",
            "http:/example.com",
            "http//example.com",
            "http://.com",
            "http://example..com",
            "http://-example.com",
            "http://example-.com",
            "http://example.c",
            "http://example.toolongtld",
            "http://192.168.0.300",  # Invalid IP
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(self.validator.is_valid_url(url))

    def test_valid_ipv4_addresses(self):
        valid_ipv4s = [
            "192.168.0.1",
            "0.0.0.0",
            "255.255.255.255",
            "10.0.0.1",
        ]
        for ipv4 in valid_ipv4s:
            with self.subTest(ipv4=ipv4):
                self.assertTrue(self.validator.is_valid_ipv4(ipv4))

    def test_invalid_ipv4_addresses(self):
        invalid_ipv4s = [
            "256.256.256.256",
            "192.168.0",
            "192.168.0.1.1",
            "192.168.0.a",
            "-1.-1.-1.-1",
            "300.300.300.300",
        ]
        for ipv4 in invalid_ipv4s:
            with self.subTest(ipv4=ipv4):
                self.assertFalse(self.validator.is_valid_ipv4(ipv4))

if __name__ == '__main__':
    unittest.main()
