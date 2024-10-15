from django.test import TestCase
from blog.utils.blacklist import is_valid_username, check_text_validity

class UsernameValidationTests(TestCase):

    def test_neutral_username(self):
        self.assertTrue(is_valid_username("Neutralname"))

    def test_whitelisted_username(self):
        self.assertTrue(is_valid_username("Testforwhite"))

    def test_blacklisted_username(self):
        self.assertFalse(is_valid_username("Testforblack"))

    def test_whitelisted_and_blacklisted_username(self):
        self.assertTrue(is_valid_username("Testforgrey"))

class TextValidationTests(TestCase):

    def test_neutral_text(self):
        is_valid, invalid_words = check_text_validity("The neutral text.")
        self.assertTrue(is_valid)
        self.assertEqual(invalid_words, [])

    def test_whitelisted_text(self):
        is_valid, invalid_words = check_text_validity("Testforwhite text.")
        self.assertTrue(is_valid)
        self.assertEqual(invalid_words, [])

    def test_blacklisted_text(self):
        is_valid, invalid_words = check_text_validity("Testforblack text.")
        self.assertFalse(is_valid)
        self.assertEqual(invalid_words, ["testforblack"])

    def test_whitelisted_and_blacklisted_text(self):
        is_valid, invalid_words = check_text_validity("Testforgrey text.")
        self.assertTrue(is_valid)
        self.assertEqual(invalid_words, [])
