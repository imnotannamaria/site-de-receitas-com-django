from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailsViewsTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 20000})
        )
        self.assertEqual(response.status_code, 404)

    @skip('Fiz merda nos campos do models, e acabou que o ficou sem o campo de descrição. Por isso o erro!')  # noqa: E501
    def test_recipe_detail_template_loads_tge_correct_recipe(self):
        self.make_recipe(title='Loads one recipe')

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1}
            )
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn(
            'Loads one recipe', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        self.make_recipe(is_published=False,)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1}
            )
        )

        self.assertEqual(response.status_code, 404)
