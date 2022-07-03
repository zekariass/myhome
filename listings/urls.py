from django.urls import path
from listings import views

urlpatterns = [
    path("listingmode/list/", views.ListingModeListView.as_view(), name="listingmode-list"),
    path("listingtype/list/", views.ListingTypeListView.as_view(), name="listingtype-list"),
    path("listingstate/list/", views.ListingStateListView.as_view(), name="listingstate-list"),

    path("create/", views.ListingListCreateView.as_view(), name="listing-create"),
    
    path("agent-listing/count/", views.AgentNumberOfListingView.as_view(), name="agent-listing-count"),
    path("list-by-property/", views.ListingListByProperty.as_view(), name="listing-list-by-property"),
    path("list-by-agent/", views.ListingListByAgent.as_view(), name="listing-list-by-agent"),
    path("public/search/", views.PublicListingListView.as_view(), name="public-listing-search"),
    path("public/<int:pk>/detail/", views.PublicListingRetrieveView.as_view(), name="public-listing-retrieve"),
    path("list-by-unit/", views.ListingListByPropertyUnit.as_view(), name="listing-list-by-unit"),

    path("<int:pk>/update/", views.MainListingRetrieveUpdateDestroyView.as_view(), name="listing-update"),
    path("<int:pk>/delete/", views.MainListingRetrieveUpdateDestroyView.as_view(), name="listing-delete"),

]