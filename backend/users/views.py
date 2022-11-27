from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework import (
    permissions, status, generics,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription
from .serializers import (
    SubscriptionSerializer, SubscriptionShowSerializers,
)


User = get_user_model()


class SubscribeView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionShowSerializers

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            following__user=user,)


class SubscribeViewSet(UserViewSet):
    @action(
        detail=True,
        methods=[
            'post',
            'delete',
        ],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = self.request.user.id
        following = int(self.kwargs['id'])
        subscribe = Subscription.objects.filter(
            user=user,
            following=following,
        )
        if request.method == 'DELETE':
            if subscribe.exists():
                subscribe.delete()
            else:
                return Response(
                    {'errors': 'Отсутствует подписка'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == 'POST':
            if user == following:
                return Response(
                    {'errors': 'Нельзя подписаться на себя!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if subscribe.exists():
                return Response(
                    {'errors': 'Подписка уже оформлена'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = SubscriptionSerializer(
                data={'user': user, 'following': following},
                context={'request': request},)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = SubscriptionShowSerializers(
                serializer.instance.following,
                context={'request': request},)
            return Response(
                response.data,
                status=status.HTTP_201_CREATED,)
        return Response(status=status.HTTP_204_NO_CONTENT)
