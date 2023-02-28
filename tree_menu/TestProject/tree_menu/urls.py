from tree_menu.views import MainPageView
from django.urls import path


urlpatterns = [
    path("", MainPageView.as_view()),
    path("<int:item_id>/", MainPageView.as_view(), name="menu"),
]
