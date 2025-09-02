from django.urls import path
from TeoNiko.jewels import views

urlpatterns = [
    path('create/', views.JewelCreateView.as_view(), name='add-jewel'),
    path('<int:pk>/<str:slug>/', views.JewelDetailView.as_view(), name='jewel-details'),
    path('qv/<int:pk>/<str:slug>/', views.JewelQuickView.as_view(), name='jewel-quick-view'),
]