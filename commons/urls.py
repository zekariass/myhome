from django.urls import path
from commons import views

urlpatterns = [
    path("country/list/", views.ListCountry.as_view(), name="country_list"),
    path("region/list/", views.ListRegionByCountry.as_view(), name="region_list"),
    path("city/list/", views.ListCityByRegion.as_view(), name="city_list"),
]
