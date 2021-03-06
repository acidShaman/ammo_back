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
from django.urls import path

from menu.views import ShowPositionsView, ShowCategoriesView, ShowPopularDishesView, CreateNewCategoryView, \
    EditCategoryView, ShowAllPositionsView, CreateNewPositionView, EditPositionView

urlpatterns = [
    path('', ShowCategoriesView.as_view()),
    path('category/new/', CreateNewCategoryView.as_view()),
    path('category/<int:id>/edit/', EditCategoryView.as_view()),
    path('few/', ShowPopularDishesView.as_view()),
    path('all/', ShowAllPositionsView.as_view()),
    path('position/new/', CreateNewPositionView.as_view()),
    path('position/<int:id>/edit/', EditPositionView.as_view()),
    path('<str:category>/', ShowPositionsView.as_view()),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
