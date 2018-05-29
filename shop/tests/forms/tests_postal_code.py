from django.test import TestCase
from ...forms import *


class TestPostalCodeValidation(TestCase):
    def test_postal_code_for_Poland_valid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertTrue(user_form.is_valid())

    def test_postal_code_for_Poland_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22932', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_postal_code_for_Poland_invalid_2(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '2-2332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "PL"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_postal_code_for_Los_Angeles_valid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "LA"}
        user_form = UserForm(data=form)
        self.assertTrue(user_form.is_valid())

    def test_postal_code_for_Los_Angeles_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "LA"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())

    def test_postal_code_for_Norway_valid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '9991', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "NO"}
        user_form = UserForm(data=form)
        self.assertTrue(user_form.is_valid())

    def test_postal_code_for_Norway_invalid(self):
        form = {'first_name': "Jan", 'last_name': "Kowalski",
                'email': "hubert.hernoga@wp.pl", 'company': "BigOne", 'city': "Florida",
                'postal_code': '22-332', 'address1': "Zone", 'address2': "Zone2",
                'phone_number': '+48509481699', 'country': "NO"}
        user_form = UserForm(data=form)
        self.assertFalse(user_form.is_valid())



if __name__ == "__main__":
    unittest.main()