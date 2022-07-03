from django.urls import path
from commons import views

urlpatterns = [
    path("country/list/", views.ListCountry.as_view(), name="country-list"),
    path("region/list/", views.ListRegionByCountry.as_view(), name="region-list"),
    path("city/list/", views.ListCityByRegion.as_view(), name="city-list"),
    path("address/<int:pk>/update/", views.AddressRetrieveUpdateDestroyView.as_view(), name="address-update"),

    path("periodicity/list/", views.PeriodicityListView.as_view(), name="periodicity-list"),
]
