from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.MyHomeUserListCreateView.as_view(), name='user-signup'),
    path('list/', views.MyHomeUserListCreateView.as_view(), name='user-list'),
    path('<int:pk>/detail/', views.MyHomeUserDetailUpdateView.as_view(), name='user-detail'),
    path('<int:pk>/update/', views.MyHomeUserDetailUpdateView.as_view(), name='user-update')
]