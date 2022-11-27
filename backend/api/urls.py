from django.urls import include, path
from rest_framework import routers

from users.views import SubscribeView, SubscribeViewSet
from .views import (
    TagsViewSet, IngredientsViewSet, RecipeViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', SubscribeViewSet, basename='user')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/subscriptions/',
        SubscribeView.as_view(),
        name='subscriptions',),
    path('', include(router.urls)),
]
