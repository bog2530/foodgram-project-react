from django.urls import include, path

app_name = 'api'


urlpatterns = [
    # path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
