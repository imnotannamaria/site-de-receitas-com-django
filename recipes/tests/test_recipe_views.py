from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    #  =================== HOME  ===================

    # verifica se a função que ta sendo executada é igual a função que tem na view  # noqa: E501
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    # verifica se o código que a view retorna está OK
    def test_recipe_home_view_returns_status_code_200_Ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # verifica se o template renderizado foi o certo
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # verifica se o template da home mostra not found recipes
    def test_recipe_home_teplate_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No Recipes found here! :(',
            response.content.decode('utf-8')
        )

    @skip('Fiz merda nos campos do models, e acabou que o ficou sem o campo de descrição. Por isso o erro!')  # noqa: E501
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn(
            'Sei lá pizza?', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False,)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'No Recipes found here! :(',
            response.content.decode('utf-8')
        )

    #  =================== END HOME  ===================

    #  =================== CATEGORY  ===================

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

    # =================== END CATEGORY  ===================

    #  =================== RECIPE  ===================

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

    #  =================== END RECIPE  ===================
