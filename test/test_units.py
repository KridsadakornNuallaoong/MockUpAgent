import hashlib
import unittest

from tools.general_tools import (add_two_numbers, divide_two_numbers,
                                 multiply_two_numbers, subtract_two_numbers)
from tools.secure_tools import (base64_decode, base64_encode, dir_list,
                                hash_string)
from tools.time_tools import get_current_time


class TestGeneralTools(unittest.TestCase):
    print("♾️ Testing General Tools...")

    def test_add_two_numbers(self):
        num_case = [
            ((2, 3), 5),
            ((-1, 1), 0),
            ((0, 0), 0),
        ]
        for (a, b), expected in num_case:
            self.assertEqual(add_two_numbers.run({"a": a, "b": b}), expected)

    print("Add Two Numbers tests passed.")

    def test_subtract_two_numbers(self):
        num_case = [
            ((5, 3), 2),
            ((1, -1), 2),
            ((0, 0), 0),
        ]
        for (a, b), expected in num_case:
            self.assertEqual(subtract_two_numbers.run({"a": a, "b": b}), expected)

    print("Subtract Two Numbers tests passed.")

    def test_multiply_two_numbers(self):
        num_case = [
            ((2, 3), 6),
            ((-1, 1), -1),
            ((0, 5), 0),
        ]
        for (a, b), expected in num_case:
            self.assertEqual(multiply_two_numbers.run({"a": a, "b": b}), expected)

    print("Multiply Two Numbers tests passed.")

    def test_divide_two_numbers(self):
        num_case = [
            ((6, 3), 2),
            ((-4, 2), -2),
            ((5, 2), 2.5),
        ]
        for (a, b), expected in num_case:
            self.assertEqual(divide_two_numbers.run({"a": a, "b": b}), expected)

    print("Divide Two Numbers tests passed.\n")

class TestSecureTools(unittest.TestCase):
    print("🔒 Testing Secure Tools...")

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
            
    print("Hash String tests passed.\n")

    def test_dir_list(self):
        # This test assumes the current directory has at least this file
        result = dir_list.run(".")
        print("Directory List Result:\n", result)
        self.assertNotEqual(len(result), 0)

        result = dir_list.run("./tools")
        print("Directory List Result:\n", result)
        self.assertNotEqual(len(result), 0)

    print("Directory List tests passed.\n")

class TestTimeTools(unittest.TestCase):
    print("🕒 Testing Time Tools...")

    def test_get_current_time(self):
        result = get_current_time.run("")
        self.assertRegex(result, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    print("Get Current Time tests passed.")

if __name__ == '__main__':
    unittest.main()