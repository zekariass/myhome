from django.urls import path
from systems import views

urlpatterns = [
    path("systemparameters/", views.SystemParameterListView.as_view(), name="system-parameters" )
]