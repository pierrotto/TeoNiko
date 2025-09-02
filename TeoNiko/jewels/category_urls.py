from django.urls import path
from TeoNiko.jewels import views

urlpatterns = [
    path('all/', views.CategoryLandingPageView.as_view(), name='category-all'),
    path('<str:name>/', views.CategoryFilterView.as_view(), name='category-by-name'),
]
