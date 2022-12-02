from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer, ShowRecipeSerializers
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    ShoppingList,
    Favorite,
    CounterIngredient,
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class CounterIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        source='ingredient.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name',
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = CounterIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class CreateCounterIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),)

    class Meta:
        model = CounterIngredient
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, amount):
        if amount < 1:
            raise serializers.ValidationError(
                'Количество ингридиента должно быть больше 0')
        return amount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        required=False,
        read_only=True
    )
    ingredients = CounterIngredientsSerializer(
        many=True,
        read_only=False,
        source='counter_ingredient',
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user.id
        return Favorite.objects.filter(
            recipe=obj.id,
            user=user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user.id
        return ShoppingList.objects.filter(
            recipe=obj.id,
            user=user,
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = CreateCounterIngredientsSerializer(
        many=True,
        source='counter_ingredient',
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'ingredients',
            'cooking_time',
            'text',
            'image',
        )

    def validate_cooking_time(self, cooking_time):
        if cooking_time <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0')
        return cooking_time

    def validate_tags(self, tags):
        tags_list = []
        if not tags:
            raise serializers.ValidationError(
                'Отсутствует тег(и)')
        for tag in tags:
            if tag.id in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальны')
            tags_list.append(tag.id)
        return tags

    def validate_ingredients(self, ingredients):
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутствуют ингридиенты')
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингридиенты должны быть уникальны')
            ingredients_list.append(ingredient['id'])
        return ingredients

    def add_ingredients(self, ingredients, recipe):
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_request = CounterIngredient(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            ingredients_list.append(ingredient_request)
        CounterIngredient.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('counter_ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(validated_data.pop('tags'))
        self.add_ingredients(
            validated_data.pop('counter_ingredient'),
            instance,
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredients = CounterIngredient.objects.filter(
            recipe=instance)
        representation['ingredients'] = CounterIngredientsSerializer(
            ingredients,
            many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags,
            many=True,
            required=False,
        ).data
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'recipe'
        )
        model = Favorite

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if not request or request.user.is_anonymous:
            return False
        if Favorite.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже добавлен'}
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        recipe = get_object_or_404(
            Recipe,
            id=instance.recipe_id,
        )
        representation = ShowRecipeSerializers(
            recipe,
            context={'request': request},
        )
        return representation.data


class ShoppingListSerializer(FavoriteSerializer):
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if not request or request.user.is_anonymous:
            return False
        if ShoppingList.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже добавлен'}
            )
        return data
