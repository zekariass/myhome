from django.contrib import admin
from listings import models as list_models

admin.site.register(list_models.PaymentMode)
admin.site.register(list_models.ListingType)
admin.site.register(list_models.ListingState)
admin.site.register(list_models.Listing)
admin.site.register(list_models.SavedListing)
admin.site.register(list_models.FeaturedListingState)
admin.site.register(list_models.FeaturedListing)