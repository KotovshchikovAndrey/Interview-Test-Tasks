from tree_menu.views import MainPageView
from django.urls import path


urlpatterns = [
    path("", MainPageView.as_view()),
]
