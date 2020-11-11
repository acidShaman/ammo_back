"""Ammo_BackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from profile.views import ShowProfileView, CreateProfileView, UpdateProfileView, CreateUpdateAddressView, \
    AppendDeleteFavoritesView, ChangePasswordView

urlpatterns = [
    path('', ShowProfileView.as_view()),
    path('register/', CreateProfileView.as_view()),
    path('<int:id>/', UpdateProfileView.as_view()),
    path('<int:user_id>/address/', CreateUpdateAddressView.as_view()),
    path('new-password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('<int:user_id>/favorites/<int:dish_id>/', AppendDeleteFavoritesView.as_view())
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
