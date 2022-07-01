from rest_framework import serializers
from listings import models as list_models
from commons import serializers as cmn_serializers
# import properties.serializers as ser

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
    address = cmn_serializers.AddressSerializer(read_only=True)
    class Meta:
        model = list_models.MainListing
        fields ="__all__"

class MainListingPublicSerializer(serializers.ModelSerializer):
    address = cmn_serializers.AddressSerializer(read_only=True)
    # property = serializers.SerializerMethodField("get_property")
    property_images = serializers.SerializerMethodField()
    # property = ser.PropertySerializer(read_only=True)
    class Meta:
        model = list_models.MainListing
        fields = ("id",
            "listing_state",
            "listing_mode",
            "property_price",
            "deposit_in_months",
            "is_approved",
            "is_expired",
            "listed_on",
            "property",
            "property_category",
            "payment",
            "listing_type",
            "listing_currency",
            "agent",
            "address",
            "property_images"
            )
    
    # def get_property(self, obj):
    #     from properties.serializers import PropertySerializer
    #     from properties.models import Property
    #     property_instance = Property.objects.get(pk=obj.property.id)
    #     property =  PropertySerializer(property_instance)
    #     return property.data
    def get_property_images(self, obj):
        from properties.serializers import PropertyImageSerializer
        from properties.models import PropertyImage
        image_instances = PropertyImage.objects.filter(property=obj.property.id)
        images =  PropertyImageSerializer(image_instances, many=True, context=self.context)
        return images.data
 

class MainListingBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.MainListing
        exclude = ("property","agent",)
#================================================================

class ApartmentUnitListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.ApartmentUnitListing
        fields = "__all__"

class CommercialPropertyUnitListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.CommercialPropertyUnitListing
        fields = "__all__"

class VillaListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.VillaListing
        fields = "__all__"

class ShareHouseListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ShareHouseListing
        fields = "__all__"

class AllPurposePropertyListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.AllPurposePropertyUnitListing
        fields = "__all__"