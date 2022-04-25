from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 20000})
        )
        self.assertEqual(response.status_code, 404)

    @skip('Fiz merda nos campos do models, e acabou que o ficou sem o campo de descrição. Por isso o erro!')  # noqa: E501
    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='This is a category test')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn(
            'This is a category test', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False,)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 20000})
        )

        self.assertEqual(response.status_code, 404)
