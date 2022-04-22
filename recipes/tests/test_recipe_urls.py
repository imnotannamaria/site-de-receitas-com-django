from django.test import TestCase
from django.urls import reverse


class RecipeUrlTest(TestCase):

    # Verfica se ta tudo bem com a url da home e se a url é uma '/'
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    # Verfica se ta tudo bem com a url de category e se a url é '/recipes/category/1/' # noqa: E501
    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    # Verfica se ta tudo bem com a url de uma recipe e se a url é '/recipes/1/'
    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')
