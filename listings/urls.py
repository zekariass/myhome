from django.urls import path
from listings import views

urlpatterns = [
    path("listingmode/list/", views.ListingModeListView.as_view(), name="listingmode-list"),
    path("listingtype/list/", views.ListingTypeListView.as_view(), name="listingtype-list"),
    path("listingstate/list/", views.ListingStateListView.as_view(), name="listingstate-list"),

    path("create/", views.ListingListCreateView.as_view(), name="listing-create"),
    
    path("agent-listing/count/", views.AgentNumberOfListingView.as_view(), name="agent-listing-count"),
]