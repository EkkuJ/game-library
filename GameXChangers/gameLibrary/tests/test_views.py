from django.test import TestCase, Client
from django.urls import reverse
from gameLibrary.models import *

class TestViews(TestCase):

    def setup(self):
        self.client = Client()
        self.game = Game.objects.create(
            name="test_game", description="for testing", url="https://distracted-pike-6aeaf9.netlify.com/"
        )
        self.user = User.objects[0]


    def test_home_GET(self):
        response = self.client.get(reverse('gameLibrary:home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameLibrary/home.html')
    
    def test_browseGames_GET(self):
        response = self.client.get(reverse('gameLibrary:browseGames'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameLibrary/browseGames.html')
    
    def test_myGames_GET(self):
        response = self.client.get(reverse('gameLibrary:myGames'))

        self.assertEquals(response.status_code, 302)
    

    def test_addGame_GET(self):
        response = self.client.get(reverse('gameLibrary:addGame'))

        self.assertEquals(response.status_code, 302)
    
    
    def test_addGame_POST(self):
        game = Game.objects.create(
            name="test_game", description="for testing", url="https://distracted-pike-6aeaf9.netlify.com/"
        )

        response = self.client.post(reverse('gameLibrary:addGame'), 
        {'name': 'test_game', 'description': 'for testing', 'url':'https://distracted-pike-6aeaf9.netlify.com/', 'price': 10})


        self.assertEquals(response.status_code, 302)
    

    def test_removeGame_GET(self):
        response = self.client.get(reverse('gameLibrary:removeGame', args=['0']))

        self.assertEquals(response.status_code, 302)
    
    def test_gameStats_GET(self):
        response = self.client.get(reverse('gameLibrary:gameStats', args=['0']))

        self.assertEquals(response.status_code, 302)
    
    def test_removeGame_GET(self):
        response = self.client.get(reverse('gameLibrary:removeGame', args=['0']))

        self.assertEquals(response.status_code, 302)
    
    def test_modifyGame_GET(self):
        response = self.client.get(reverse('gameLibrary:modifyGame', args=['0']))

        self.assertEquals(response.status_code, 302)
    
    def test_buyGame_GET(self):
        response = self.client.get(reverse('gameLibrary:buyGame', args=['0']))

        self.assertEquals(response.status_code, 302)