from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subscription
from recipes.models import Recipe

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user.id,
            following=obj.id,
        ).exists()


class ShowRecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'user',
            'following',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'following'))
        ]


class SubscriptionShowSerializers(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(
        read_only=True)
    recipes_count = serializers.SerializerMethodField(
        read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = Recipe.objects.filter(
                author=obj
            ).all()[:(int(limit))]
        else:
            recipes = Recipe.objects.filter(
                author=obj
            ).all()
        context = {'request': request}
        return ShowRecipeSerializers(
            recipes, many=True, context=context
        ).data
