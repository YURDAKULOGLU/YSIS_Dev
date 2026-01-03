import re


class URLValidator:
    """
    A class to validate URLs and IPv4 addresses.
    """

    def __init__(self):
        # Regex pattern for validating a URL
        self.url_pattern = re.compile(
            r'^(https?|ftp)://'  # http://, https://, or ftp://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # Regex pattern for validating an IPv4 address
        self.ipv4_pattern = re.compile(
            r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

    def is_valid_url(self, url: str) -> bool:
        """
        Validates if the given URL is valid.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        return re.match(self.url_pattern, url) is not None

    def is_valid_ipv4(self, ipv4: str) -> bool:
        """
        Validates if the given IPv4 address is valid.

        Args:
            ipv4 (str): The IPv4 address to validate.

        Returns:
            bool: True if the IPv4 address is valid, False otherwise.
        """
        return re.match(self.ipv4_pattern, ipv4) is not None
