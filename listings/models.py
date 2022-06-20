from django.db import models
from django.utils import timezone
import properties.models as prop_models
from payments import models as pymnt_models
from agents import models as agent_models
from systems import models as sys_models
from django.conf import settings

"""A listing mode can be selected automatically appropriate for the current user. 
    A listing can be free of any charge, subscription-based, or payment mode"""
class ListingMode(models.Model):
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
        return self.state


"""Listing is postings of properties with a specific listing type. The listing can be either for rent or sale"""
class MainListing(models.Model):

    LISTING_MODES = [ 
        ("SUBSCRIPTION", "Subscription"),
        ("PAY_PER_LISTING", "Pay-per-listing"),
    ]

    LISTING_STATES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("EXPIRED", "Expired"),
    ]

    property = models.ForeignKey(prop_models.Property, on_delete=models.CASCADE, related_name="listings")
    payment = models.OneToOneField(pymnt_models.Payment, on_delete=models.SET_NULL, null=True, related_name="listing")
    listing_type = models.ForeignKey(ListingType, on_delete=models.SET_NULL, null=True, related_name="listings_in_this_type")
    # listing_state = models.ForeignKey(ListingState, on_delete=models.SET_NULL, null=True, related_name="listings_in_this_state")
    # listing_mode = models.ForeignKey(ListingMode, on_delete=models.SET_NULL, null=True, related_name="listings_in_this_mode")
    listing_state = models.CharField(max_length=50, choices=LISTING_STATES, default=LISTING_STATES[1][0])
    listing_mode = models.CharField(max_length=50, choices=LISTING_MODES, default=LISTING_MODES[1][0], null=True)
    property_price = models.FloatField(verbose_name="property price", default=0.00)
    listing_currency = models.ForeignKey(sys_models.Currency ,verbose_name="property price currency type", on_delete=models.SET_NULL, null=True)
    deposit_in_months = models.SmallIntegerField(verbose_name="number of months that deposit is required", default=0)
    is_approved = models.BooleanField(default=False)
    agent = models.ForeignKey(agent_models.Agent, on_delete=models.CASCADE, verbose_name='agent who creates this listing', null=True, blank=True)
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.agent = self.property.agent
        if self.payment:
            if self.payment.payment_method.cat_key == "PM04":
                self.listing_mode = "SUBSCRIPTION"
            else:
                self.listing_mode = "PAY_PER_LISTING"
        super(MainListing, self).save(*args, **kwargs)


"""Normal users may save a listing for checking later"""
class SavedListing(models.Model):
    main_listing = models.ForeignKey(MainListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_listing")
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
    main_listing = models.ForeignKey(MainListing, on_delete=models.CASCADE, related_name="features")
    feature_payment = models.OneToOneField(pymnt_models.Payment, on_delete=models.CASCADE)
    featured_listing_state = models.ForeignKey(FeaturedListingState, on_delete=models.SET_DEFAULT, default="EXPIRED")
    featured_on = models.DateTimeField(default=timezone.now, editable=False)
    expire_on = models.DateTimeField(editable=True, null=False, blank=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=["main_listing","featured_listing_state"], name="single_state_featured_listing")
    #     ]


#NEWLY ADDED TABLES FOR LISTING BY PROPERTY CATEGORY

class ApartmentUnitListing(models.Model):
    apartment_unit = models.ForeignKey(prop_models.ApartmentUnit, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="apartment_unit_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class CommercialPropertyUnitListing(models.Model):
    commercial_property_unit = models.ForeignKey(prop_models.CommercialPropertyUnit, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="commercial_property_unit_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class AllPurposePropertyUnitListing(models.Model):
    all_purpose_property_unit = models.ForeignKey(prop_models.AllPurposePropertyUnit, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="all_purpose_property_unit_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class CondominiumListing(models.Model):
    condominium = models.ForeignKey(prop_models.Condominium, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="condominium_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class TraditionalHouseListing(models.Model):
    traditional_house = models.ForeignKey(prop_models.TraditionalHouse, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="traditional_house_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class ShareHouseListing(models.Model):
    Share_house = models.ForeignKey(prop_models.ShareHouse, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="Share_house_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class VillaListing(models.Model):
    villa = models.ForeignKey(prop_models.Villa, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="villa_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class OfficeListing(models.Model):
    office = models.ForeignKey(prop_models.Office, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="office_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class HallListing(models.Model):
    hall = models.ForeignKey(prop_models.Hall, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="hall_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)

class LandListing(models.Model):
    land = models.ForeignKey(prop_models.Land, on_delete=models.CASCADE, related_name="listings")
    main_listing = models.OneToOneField(MainListing, on_delete=models.CASCADE, related_name="land_listing")
    listed_on = models.DateTimeField(default=timezone.now, editable=False)