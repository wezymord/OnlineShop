from django.test import TestCase
from ...forms import *


class TestEmailValidation(TestCase):
    def test_phone_number_expect_to_be_valid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert34123@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertTrue(user_form.is_valid())

    def test_phone_number_incorrect_prefix_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_phone_number_without_prefix_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_phone_number_with_dash_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '509-481-699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_phone_number_with_letter_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48d094h1699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_phone_number_too_short_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+4850948169', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

if __name__ == "__main__":
    unittest.main()