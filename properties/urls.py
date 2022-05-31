from django.urls import path
from properties import views

urlpatterns = [
    path('categories/', views.PropertyCategoryListCreateView.as_view(), name="property-category-list"),
    path('create/', views.PropertyListCreateView.as_view(), name="property-cteate"),
    path('list-by-agent/', views.PropertyListByAgentView.as_view(), name="property-list-by-agent"),
    path('<int:pk>/detail/', views.PropertyRetrieveDestroyAPIView.as_view(), name="property-detail"),
    path('<int:pk>/update/', views.PropertyUpdateAPIView.as_view(), name="property-update"),
    path('housetypes/', views.HouseTypeListCreateView.as_view(), name="house-type-list"),
    path('buildingtypes/', views.BuildingTypeListCreateView.as_view(), name="building-type-list"),
    path('image/create/', views.PropertyImageListCreateView.as_view(), name="property-image-create"),
    path('image/<int:pk>/delete/', views.PropertyImageRetrieveUpdateDestroy.as_view(), name="property-image-delete"),
    path('video/create/', views.PropertyVideoListCreateView.as_view(), name="property-video-create"),
    path('video/<int:pk>/delete/', views.PropertyVideoRetrieveUpdateDestroy.as_view(), name="property-video-delete"),
    path('file/labels/', views.PropertyFileLabelListCreateView.as_view(), name="property-file-label-list"),
    path('file/<int:pk>/update/', views.PropertyImageRetrieveUpdateDestroy.as_view(), name="property-image-update"),
    path('edufalevel/list/', views.EduFaLevelListView.as_view(), name="edufalevel-list"),
    path('<int:pk>/edufa/create/', views.EducationFacilityListCreateView.as_view(), name="edufa-create"),
]