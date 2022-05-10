from django.urls import path
from properties import views

urlpatterns = [
    path('categories/', views.PropertyCategoryListCreateView.as_view(), name="property-category-list"),
    path('create/', views.PropertyListCreateView.as_view(), name="property-cteate"),
]