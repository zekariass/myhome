from django.contrib import admin
from listings import models as list_models

admin.site.register(list_models.ListingMode)
admin.site.register(list_models.ListingType)
admin.site.register(list_models.ListingState)
admin.site.register(list_models.MainListing)
admin.site.register(list_models.SavedListing)
admin.site.register(list_models.FeaturePrice)
admin.site.register(list_models.FeaturedListing)
admin.site.register(list_models.ApartmentUnitListing)
admin.site.register(list_models.CommercialPropertyUnitListing)
admin.site.register(list_models.AllPurposePropertyUnitListing)
admin.site.register(list_models.CondominiumListing)
admin.site.register(list_models.TraditionalHouseListing)
admin.site.register(list_models.ShareHouseListing)
admin.site.register(list_models.VillaListing)
admin.site.register(list_models.OfficeListing)
admin.site.register(list_models.HallListing)
admin.site.register(list_models.LandListing)
