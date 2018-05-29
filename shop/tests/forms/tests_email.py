from django.test import TestCase
from ...forms import *


class TestValidations(TestCase):
    def test_email_expect_to_be_valid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertTrue(user_form.is_valid())

    def test_email_expect_to_be_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_email_expect_to_be_invalid_2(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert3423@wppl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())


if __name__ == "__main__":
    unittest.main()