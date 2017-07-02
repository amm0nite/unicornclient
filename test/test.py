# pylint: disable=C0103

import unittest

from unicornclient import parser
from unicornclient import message

class ParserTest(unittest.TestCase):
    def setUp(self):
        my_message = message.Message()
        my_message.set_header({'message':'hello world'})
        my_message.set_body(b'1234567890')
        self.my_message = my_message

    def test_one_message(self):
        my_parser = parser.Parser()
        parsed = my_parser.parse(self.my_message.encode())

        self.assertEqual(parsed.header, self.my_message.header)
        self.assertEqual(parsed.body, self.my_message.body)

    def test_one_message_with_remaining(self):
        my_parser = parser.Parser()
        extra_data = b'112233445566'
        parsed = my_parser.parse(self.my_message.encode() + extra_data)

        self.assertEqual(parsed.header, self.my_message.header)
        self.assertEqual(parsed.body, self.my_message.body)
        self.assertEqual(my_parser.remaining, extra_data)

    def test_split_message(self):
        my_parser = parser.Parser()
        binary_string = self.my_message.encode()
        first_parsed = my_parser.parse(binary_string[:10])
        second_parsed = my_parser.parse(binary_string[10:])

        self.assertIsNone(first_parsed)
        self.assertEqual(second_parsed.header, self.my_message.header)
        self.assertEqual(second_parsed.body, self.my_message.body)

    def test_two_message(self):
        message1 = message.Message()
        message1.set_header({'message':'hello world 1'})
        message1.set_body(b'1111')
        message2 = message.Message()
        message2.set_header({'message':'hello world 2'})
        message2.set_body(b'2222')

        my_parser = parser.Parser()

        first_parsed = my_parser.parse(message1.encode() + message2.encode())

        self.assertEqual(first_parsed.header, message1.header)
        self.assertEqual(first_parsed.body, message1.body)
        self.assertEqual(my_parser.remaining, message2.encode())

        second_parsed = my_parser.parse(b'')

        self.assertEqual(second_parsed.header, message2.header)
        self.assertEqual(second_parsed.body, message2.body)
        self.assertEqual(my_parser.remaining, b'')

if __name__ == '__main__':
    unittest.main()
