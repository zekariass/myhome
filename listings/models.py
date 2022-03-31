from django.db import models
from django.utils import timezone
from properties import models as prty_models
from payments import models as pymnt_models
from django.conf import settings

"""A payment mode can be selected automatically appropriate for the current user. 
    A listing can be free of any charge, subscription-based, or payment mode"""
class PaymentMode(models.Model):
    mode = models.CharField(verbose_name="payment mode", max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.mode


"""Listing can be either for rent or for sale. The listing type is selected during 
    listing a registered property, not during registering the property"""
class ListingType(models.Model):
    type = models.CharField(verbose_name="listing type", max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type


"""A listing has a specific state at any time, such as suspended, active, inactive, expired, etc"""
class ListingState(models.Model):
    state = models.CharField(verbose_name="listing state", max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type


"""Listing is postings of properties with a specific listing type. The listing can be either for rent or sale"""
class Listing(models.Model):
    property = models.ForeignKey(prty_models.Property, on_delete=models.CASCADE, related_name="listed_properties")
    payment = models.OneToOneField(pymnt_models.Payment, on_delete=models.CASCADE, related_name="listing")
    listing_type = models.ForeignKey(ListingType, on_delete=models.CASCADE, related_name="listings_in_this_type")
    listing_state = models.ForeignKey(ListingState, on_delete=models.CASCADE, related_name="listings_in_this_state")
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.CASCADE, related_name="listings_in_this_mode")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)


"""Normal users may save a listing for checking later"""
class SavedListing(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_by_user")
    saved_on = models.DateTimeField(default=timezone.now, editable=False)


"""Each featured listing has a specific state, such as active, inactive, expired, etc"""
class FeaturedListingState(models.Model):
    state = models.CharField(verbose_name="featured listing state", max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.state

"""An agent may pay more to feature their specific listing. When a listing is featured, it will show up 
    on more searches than normal searches and allows it to be listed on the landing page"""
class FeaturedListing(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    feature_payment = models.OneToOneField(pymnt_models.Payment, on_delete=models.CASCADE)
    featured_listing_state = models.ForeignKey(FeaturedListingState, on_delete=models.SET_DEFAULT, default="EXPIRED")
    featured_on = models.DateTimeField(default=timezone.now, editable=False)
    expire_on = models.DateTimeField(editable=True, null=False, blank=False)
