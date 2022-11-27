from django.contrib import admin
from django.contrib.auth.admin import Group

from .models import (
    Ingredient, Tag, Recipe,
    CounterIngredient, ShoppingList, Favorite,
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = '--None--'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'add_in_favorites',
    )
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'tags',)
    empty_value_display = '--None--'
    readonly_fields = ('add_in_favorites',)

    def add_in_favorites(self, obj):
        return obj.favorites_list.count()


class CounterIngredientAdmin(admin.ModelAdmin):
    empty_value_display = '--None--'


class ShoppingListAdmin(admin.ModelAdmin):
    empty_value_display = '--None--'


class FavoritAdmin(admin.ModelAdmin):
    empty_value_display = '--None--'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CounterIngredient, CounterIngredientAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoritAdmin)

admin.site.unregister(Group)
