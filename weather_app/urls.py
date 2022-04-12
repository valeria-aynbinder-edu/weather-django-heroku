from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # path("subscriptions/", views.subscriptions),
    path("users/current", views.current_user),
    path("subscriptions", views.subscriptions),
    path("subscriptions/<int:id>", views.subscription_details),
    path("subscriptions/import", views.subscription_import),
    path("download", views.download_file),
    path("countries", views.get_countries_capitals),
    # path("users/<pk:int>", views.current_user),
    # path("user_settings/current", views.current_user_settings),

    path('token/', obtain_auth_token),
    # adding DELETE to token
]