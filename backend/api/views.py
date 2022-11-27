from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets, permissions, status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Ingredient, Tag, Recipe,
    ShoppingList, Favorite, CounterIngredient,
)
from .mixins import ReadingMixins
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeCreateSerializer,
    RecipeSerializer, FavoriteSerializer, ShoppingListSerializer
)
from .utils import table_ricipes
from .filter import RecipeFilter, IngredientFilter
from .permissions import IsOwnerOrReadOnly
from .paginations import RecipePagination

User = get_user_model()


class TagsViewSet(ReadingMixins):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientsViewSet(ReadingMixins):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_ricipes(
            self, request, serializer_selection, model):
        user = self.request.user.id
        ricipes = int(self.kwargs['pk'])
        data_model = model.objects.filter(
            user=user,
            recipe=ricipes,
        )
        if request.method == 'DELETE':
            if data_model.exists():
                data_model.delete()
            else:
                return Response(
                    {'errors': 'Отсутствует рецепт'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'POST':
            if data_model.exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = serializer_selection(
                data={'user': user, 'recipe': ricipes},
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=[
            'post',
            'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        return self.add_ricipes(
            request,
            FavoriteSerializer,
            Favorite,
        )

    @action(
        detail=True,
        methods=[
            'post',
            'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        return self.add_ricipes(
            request,
            ShoppingListSerializer,
            ShoppingList,
        )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_list.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        filename = 'ingredients.txt'
        ingredients = CounterIngredient.objects.filter(
            recipe__shopping_list__user=user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        table = table_ricipes(ingredients)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response.write(table)
        data_model = ShoppingList.objects.filter(user=user.id)
        data_model.delete()
        return response
