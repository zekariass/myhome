from django.urls import path
from agents import views


urlpatterns = [
    path("create/", views.AgentCreateView.as_view(), name="agent_create")
]