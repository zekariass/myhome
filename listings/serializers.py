from rest_framework import serializers
from listings import models as list_models

class ListingModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingMode
        fields = "__all__"

class ListingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingType
        fields = "__all__"

class ListingStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingState
        fields = "__all__"

#==========MAIN LISTING=========================================
class MainListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.MainListing
        fields = "__all__"

class MainListingBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.MainListing
        exclude = ("property","agent",)
#================================================================

class ApartmentUnitListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ApartmentUnitListing
        fields = "__all__"

class CommercialPropertyUnitListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.CommercialPropertyUnitListing
        fields = "__all__"

class VillaListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.VillaListing
        fields = "__all__"