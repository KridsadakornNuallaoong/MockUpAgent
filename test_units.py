import hashlib
import unittest

from tools.secure_tools import base64_decode, base64_encode, hash_string


class TestSecureTools(unittest.TestCase):
    print("Testing Secure Tools...")

    def test_base64_encode(self):
        word_case = [
            ("Hello", "SGVsbG8="),
            ("Test String", "VGVzdCBTdHJpbmc="),
            ("Python3.8", "UHl0aG9uMy44"),
        ]
        for raw_str, expected in word_case:
            self.assertEqual(base64_encode.run(raw_str), expected)

    print("Base64 Encode tests passed.")

    def test_base64_decode(self):
        word_case = [
            ("SGVsbG8=", "Hello"),
            ("VGVzdCBTdHJpbmc=", "Test String"),
            ("UHl0aG9uMy44", "Python3.8"),
        ]
        for encoded_str, expected in word_case:
            self.assertEqual(base64_decode.run(encoded_str), expected)

    print("Base64 Decode tests passed.")

    def test_hash_string(self):
        word_case = [
            ("Hello", hashlib.sha256("Hello".encode('utf-8')).hexdigest()),
            ("Test String", hashlib.sha256("Test String".encode('utf-8')).hexdigest()),
            ("Python3.8", hashlib.sha256("Python3.8".encode('utf-8')).hexdigest()),
        ]
        for raw_str, expected in word_case:
            self.assertEqual(hash_string.run(raw_str), expected)
            
    print("Hash String tests passed.")

if __name__ == '__main__':
    unittest.main()