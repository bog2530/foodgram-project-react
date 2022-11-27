from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
        'date_joined',
    )
    search_fields = ('^email',)
    list_filter = ('email', 'first_name')
    empty_value_display = '--None--'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following'
    )
    search_fields = ('user',)
    list_filter = ('user', 'following')
    empty_value_display = '--None--'


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
