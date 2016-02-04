import json
import unittest

from hgijson.json.primitive import StrJSONEncoder, FloatJSONDecoder, IntJSONDecoder, StrJSONDecoder


class TestStrJSONEncoder(unittest.TestCase):
    """
    Tests for `StrJSONEncoder`.
    """
    def test_decode_with_int(self):
        self.assertEqual(StrJSONEncoder().default(123), "123")

    def test_decode_with_float(self):
        self.assertEqual(StrJSONEncoder().default(12.3), "12.3")


class TestIntJSONDecoder(unittest.TestCase):
    """
    Tests for `IntJSONDecoder`.
    """
    def test_default_with_int_as_string(self):
        self.assertEqual(IntJSONDecoder().decode("123"), 123)

    def test_with_json_loads_and_int_as_string(self):
        self.assertEqual(json.loads("123", cls=IntJSONDecoder), 123)


class TestFloatJSONDecoder(unittest.TestCase):
    """
    Tests for `FloatJSONDecoder`.
    """
    def test_default_with_float_as_string(self):
        self.assertEqual(FloatJSONDecoder().decode("12.3"), 12.3)

    def test_with_json_loads_and_int_as_string(self):
        self.assertEqual(json.loads("12.3", cls=FloatJSONDecoder), 12.3)


class TestStrJSONDecoder(unittest.TestCase):
    """
    Tests for `TestStrJSONDecoder`.
    """
    def test_default_with_string(self):
        self.assertEqual(StrJSONDecoder().decode("123"), "123")

    def test_with_json_loads_and_string(self):
        self.assertEqual(json.loads("123", cls=StrJSONDecoder), "123")


if __name__ == "__main__":
    unittest.main()