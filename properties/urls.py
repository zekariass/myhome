from django.urls import path
from properties import views

urlpatterns = [
    path('categories/', views.PropertyCategoryListCreateView.as_view(), name="property-category-list"),
    path('create/', views.PropertyListCreateView.as_view(), name="property-cteate"),
    path('housetypes/', views.HouseTypeListCreateView.as_view(), name="house-type-list"),
    path('buildingtypes/', views.BuildingTypeListCreateView.as_view(), name="building-type-list"),
    path('image/create/', views.PropertyImageListCreateView.as_view(), name="property-image-create"),
    path('image/<int:pk>/delete/', views.PropertyImageRetrieveUpdateDestroy.as_view(), name="property-image-delete"),
    path('video/create/', views.PropertyVideoListCreateView.as_view(), name="property-video-create"),
    path('video/<int:pk>/delete/', views.PropertyVideoRetrieveUpdateDestroy.as_view(), name="property-video-delete"),
    path('file/labels/', views.PropertyFileLabelListCreateView.as_view(), name="property-file-label-list"),
    path('file/<int:pk>/update/', views.PropertyImageRetrieveUpdateDestroy.as_view(), name="property-image-update"),
]