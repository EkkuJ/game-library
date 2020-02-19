from django.test import SimpleTestCase
from django.urls import reverse, resolve
from gameLibrary.views import *


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('gameLibrary:home')
        self.assertEquals(resolve(url).func, home)

    def test_browseGames_url_is_resolved(self):
        url = reverse('gameLibrary:browseGames')
        self.assertEquals(resolve(url).func, browseGames)

    def test_myGames_url_is_resolved(self):
        url = reverse('gameLibrary:myGames')
        self.assertEquals(resolve(url).func, myGames)

    def test_developedGames_url_is_resolved(self):
        url = reverse('gameLibrary:developedGames')
        self.assertEquals(resolve(url).func, developedGames)

    def test_addGame_url_is_resolved(self):
        url = reverse('gameLibrary:addGame')
        self.assertEquals(resolve(url).func, addGame)

    def test_api_url_is_resolved(self):
        url = reverse('gameLibrary:api')
        self.assertEquals(resolve(url).func, api)

    def test_success_url_is_resolved(self):
        url = reverse('gameLibrary:success')
        self.assertEquals(resolve(url).func, success)

    def test_error_url_is_resolved(self):
        url = reverse('gameLibrary:error')
        self.assertEquals(resolve(url).func, error)
    
    def test_playGame_url_is_resolved(self):
        url = reverse('gameLibrary:playGame', args=['0'])
        self.assertEquals(resolve(url).func, playGame)
    
    def test_removeGame_url_is_resolved(self):
        url = reverse('gameLibrary:removeGame', args=['0'])
        self.assertEquals(resolve(url).func, removeGame)
    
    def test_modifyGame_url_is_resolved(self):
        url = reverse('gameLibrary:modifyGame', args=['0'])
        self.assertEquals(resolve(url).func, modifyGame)
    
    def test_gameStats_url_is_resolved(self):
        url = reverse('gameLibrary:gameStats', args=['0'])
        self.assertEquals(resolve(url).func, gameStats)
    
    def test_buyGame_url_is_resolved(self):
        url = reverse('gameLibrary:buyGame', args=['0'])
        self.assertEquals(resolve(url).func, buyGame)
    
    def test_preview_url_is_resolved(self):
        url = reverse('gameLibrary:preview', args=['0'])
        self.assertEquals(resolve(url).func, preview)
    

