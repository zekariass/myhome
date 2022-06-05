from attr import fields
from rest_framework import serializers
from sympy import source
from properties import models as prop_models
from commons import serializers as cmn_serializers
from agents import serializers as agnt_serializers
from properties import relations



#===========APARTMENT======================================================================

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        fields = "__all__"

class ApartmentCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        exclude = ("property",)

class ApartmentUnitSerializer(serializers.ModelSerializer):
    apartment = ApartmentCreateBasicSerializer()
    class Meta:
        model = prop_models.ApartmentUnit
        fields = "__all__"

class ApartmentUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnit
        exclude = ("apartment",)
#===========CONDOMINIUM====================================================================
class CondominiumCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Condominium
        exclude = ("property",)
#===========VILLA==========================================================================
class VillaCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Villa
        exclude = ("property",)
#===========TRADITIONAL HOUSE==============================================================
class TraditionalHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TraditionalHouse
        exclude = ("property",)
#===========SHARE HOUSE====================================================================
class ShareHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ShareHouse
        exclude = ("property",)
#===========COMMERCIAL PROPERTY============================================================
class CommercialPropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialProperty
        exclude = ("property",)

class CommercialPropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialPropertyUnit
        exclude = ("commercial_property",)
#===========LAND===========================================================================
class LandCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Land
        exclude = ("property",)
#===========ALL PURPOSE PROPERTY===========================================================
class AllPurposePropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposeProperty
        exclude = ("property",)

class AllPurposePropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposePropertyUnit
        exclude = ("all_purpose_property",)
#===========HALL===========================================================================
class HallCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Hall
        exclude = ("property",)
#===========OFFICE=========================================================================
class OfficeCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Office
        exclude = ("property",)
#===============================================================================================
class PropSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Property
        fields = "__all__"
#===========EDUCATION FACILITY LEVEL=============================================================
class EdufaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EdufaLevel
        fields = "__all__"
#===========EDUCATION FACILITY=============================================================
class EducationFacilitySerializer(serializers.ModelSerializer):
    edufa_level = EdufaLevelSerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
        # fields = ("id","edufa_level","name","ownership","distance_from_property","distance_unit","description","added_on", "property")

class EducationFacilityBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
#===========TRANSPORT FACILITY========================================================
class TransFaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TransFaCategory
        fields = "__all__"

class TransportFacilitySerializer(serializers.ModelSerializer):
    trans_fa_category = TransFaCategorySerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.TransportFacility
        fields = "__all__"

class TransportFacilityBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TransportFacility
        fields = "__all__"
#===========POINT OF INTEREST =====================================================
class POICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.POICategory
        fields = "__all__"

class PointOfInterestSerializer(serializers.ModelSerializer):
    poi_category = POICategorySerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.PointOfInterest
        fields = "__all__"

class POIBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PointOfInterest
        fields = "__all__"

#=========================================================================================
class AmenityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AmenityCategory
        fields = "__all__"

class AmenitySerializer(serializers.ModelSerializer):
    category = AmenityCategorySerializer()
    class Meta:
        model = prop_models.Amenity
        fields = "__all__"

#===========Rule===========================================================================
class RuleSerializer(serializers.ModelSerializer):
    # property = PropertyCreateBasicSerializer()
    class Meta:
        model = prop_models.Rule
        exclude = ("property",)

#===========PROPERTY=======================================================================

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyImage
        exclude = ("property",)

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyVirtualTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVirtualTour
        exclude = ("property",)

class PropertyCategorySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(read_only=True, many=True)
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"

class PropertyCategorySlugSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(read_only=True, many=True)
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"
        lookup_field = "cat_key"

class PropertyCreateBasicSerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField(read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    virtual_tours_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = prop_models.Property
        fields = ["id","is_residential","description", "added_on","images_count", "videos_count","virtual_tours_count"]
        extra_kwargs = {'added_on': {'read_only': True}, "id":{"read_only":True}}

    def get_images_count(self, property):
        return property.images.count()

    def get_videos_count(self, instance):
        return instance.videos.count()

    def get_virtual_tours_count(self, instance):
        return instance.virtual_tours.count()

class PropertySerializer(serializers.ModelSerializer):
    property_category = PropertyCategorySerializer()
    address = cmn_serializers.AddressSerializer(read_only=True)
    agent = agnt_serializers.AgentSerializer(read_only=True)
    education_facility = EducationFacilitySerializer(many=True,read_only=True)
    transport_facility = TransportFacilitySerializer(many=True,read_only=True)
    point_of_interest = PointOfInterestSerializer(many=True,read_only=True)
    amenity = AmenitySerializer(many=True,read_only=True)
    rules = RuleSerializer(read_only=True, many=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    virtual_tours = PropertyVirtualTourSerializer(many=True, read_only=True)
    virtual_tours_count = serializers.SerializerMethodField(read_only=True)
    # villa = VillaSerializer(read_only=True)
    related_property = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = prop_models.Property
        fields = ["id","property_category","agent","address","is_residential","description", "agent",\
            "added_on","education_facility","transport_facility","point_of_interest","amenity", "rules",\
            "images","videos","virtual_tours", "images_count","videos_count","virtual_tours_count", "related_property"]
            # "villa","apartment","condominium","traditional_house","share_house","commercial_property",\
            # "all_purpose_property","office","hall","land"]

        extra_kwargs = {'added_on': {'read_only': True}}

    def get_images_count(self, instance):
        return instance.images.count()
    
    def get_videos_count(self, instance):
        return instance.videos.count()

    def get_virtual_tours_count(self, instance):
        return instance.virtual_tours.count()

    def get_related_property(self, instance):
        if hasattr(instance, "villa"):
            return VillaCreateBasicSerializer(instance=prop_models.Villa.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "apartment"):
            return ApartmentCreateBasicSerializer(instance=prop_models.Apartment.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "condominium"):
            return CondominiumCreateBasicSerializer(instance=prop_models.Condominium.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "traditional_house"):
            return TraditionalHouseCreateBasicSerializer(instance=prop_models.TraditionalHouse.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "share_house"):
            return ShareHouseCreateBasicSerializer(instance=prop_models.ShareHouse.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "commercial_property"):
            return CommercialPropertyCreateBasicSerializer(instance=prop_models.CommercialProperty.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "all_purpose_property"):
            return AllPurposePropertyCreateBasicSerializer(instance=prop_models.AllPurposeProperty.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "office"):
            return OfficeCreateBasicSerializer(instance=prop_models.Office.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "hall"):
            return HallCreateBasicSerializer(instance=prop_models.Hall.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "land"):
            return LandCreateBasicSerializer(instance=prop_models.Land.objects.get(property=instance.id),read_only=True).data
        else: return None

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyFileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyFileLabel
        fields = "__all__"

#===========HOUSE TYPE=====================================================================
class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.HouseType
        fields = "__all__"
#===========BUILDING TYPE==================================================================
class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.BuildingType
        fields = "__all__"

#===========LISTING DISCOUNT BY CATEGORY==================================================================
class ListingDiscountByCategorySerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    class Meta:
        model = prop_models.ListingDiscountByCategory
        fields = "__all__"
