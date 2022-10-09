from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from django.db import models

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed',
        )
        # read_only_fields = ('is_subscribed',)

        # def get_is_subscribed(self):
        #     ...


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follower',
        ),)
