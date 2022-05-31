from django.urls import path
from agents import views


urlpatterns = [
    path("create/", views.AgentCreateView.as_view(), name="agent-create"),
    path("logo/upload/", views.AgentLogoCreateView.as_view(), name="agent-logo-upload"),
    path("logo/<int:pk>/delete/", views.AgentLogoRetrieveUpdateDestroyView.as_view(), name="agent-logo-delete"),
    path("get/", views.AgentRetrieveView.as_view(), name="agent-get-full"),
    path("logo/<int:pk>/", views.AgentLogoRetrieveUpdateDestroyView.as_view(), name="agent-logo-retrieve")
]