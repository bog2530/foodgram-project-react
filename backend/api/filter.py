from django.contrib.auth import get_user_model
from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),)
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',)
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )
        ordering = ('id',)

    def filter_is_favorited(
            self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                favorites_list__user=self.request.user,)
        return queryset

    def filter_is_in_shopping_cart(
            self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                shopping_list__user=self.request.user,)
        return queryset
