from django.urls import path
from properties import views

urlpatterns = [
    path('categories/', views.PropertyCategoryListCreateView.as_view(), name="property-category-list"),
    path('create/', views.PropertyListCreateView.as_view(), name="property-cteate"),
    path('housetypes/', views.HouseTypeListCreateView.as_view(), name="house-type-list"),
    path('buildingtypes/', views.BuildingTypeListCreateView.as_view(), name="building-type-list"),
]