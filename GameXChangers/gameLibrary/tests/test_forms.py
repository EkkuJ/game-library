from django.test import TestCase
from gameLibrary.forms import GameForm


class TestForms(TestCase):
    
    def test_game_form_valid_data(self):
        form = GameForm(data={
            'name': 'test',
            'description': 'testing',
            'url': 'https://distracted-pike-6aeaf9.netlify.com/',
            'price': 100
        })

        self.assertTrue(form.is_valid())

    
    def test_game_form_no_data(self):
        form = GameForm(data={})

        self.assertFalse(form.is_valid())