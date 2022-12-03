from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=254,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=254,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=254,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=16,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=254,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Название',
        max_length=254,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        'Описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='CounterIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[
            validators.MinValueValidator(
                1,
                message='Время приготовления должно быть больше 1',
            )]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class CounterIngredient(models.Model):
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            validators.MinValueValidator(
                1,
                message='Количество должно быть больше 1',
            )]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='counter_ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='counter_ingredient',
    )

    class Meta:
        verbose_name = 'Счетчик ингридиентов'
        verbose_name_plural = 'Счетчик ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient}, {self.amount}, {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_list',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites_list',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorites_list'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.user}'
