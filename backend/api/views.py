from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import (viewsets, filters, permissions)
from rest_framework.response import Response

from recipes.models import (
    Ingredient, Tag, Recipe, ShoppingList, Favorites
)
from users.models import Subscription
from .mixins import CreateListDestroyMixins


User = get_user_model()

class FollowViewSet(CreateListDestroyMixins):
    ...


class RecipeViewSet(viewsets.ModelViewSet):
    ...
