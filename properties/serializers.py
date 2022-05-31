from attr import fields
from rest_framework import serializers
from sympy import source
from properties import models as prop_models
from commons import serializers as cmn_serializers
from agents import serializers as agnt_serializers

#===============================================================================================
# class PropSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = prop_models.Property
#         fields = "__all__"
#===========EDUCATION FACILITY LEVEL=============================================================
class EdufaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EdufaLevel
        fields = "__all__"
#===========EDUCATION FACILITY=============================================================
class EducationFacilitySerializer(serializers.ModelSerializer):
    edufa_level = EdufaLevelSerializer()
    # property = PropSerializer(write_only=True)
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
        # fields = ("id","edufa_level","name","ownership","distance_from_property","distance_unit","description","added_on", "property")

class EducationFacilityBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
#===========TRANSPORT FACILITY TYPE========================================================
class TransFaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TransFaCategory
        fields = "__all__"
#===========TRANSPORT FACILITY=============================================================
class TransportFacilitySerializer(serializers.ModelSerializer):
    trans_fa_category = TransFaCategorySerializer()
    class Meta:
        model = prop_models.TransportFacility
        fields = "__all__"
#===========POINT OF INTEREST CATEGORY=====================================================
class POICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.POICategory
        fields = "__all__"
#===========POINT OF INTEREST=============================================================
class PointOfInterestSerializer(serializers.ModelSerializer):
    poi_category = POICategorySerializer()
    class Meta:
        model = prop_models.PointOfInterest
        fields = "__all__"

#===========POINT OF INTEREST CATEGORY=====================================================
class AmenityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AmenityCategory
        fields = "__all__"
#===========POINT OF INTEREST=============================================================
class AmenitySerializer(serializers.ModelSerializer):
    category = AmenityCategorySerializer()
    class Meta:
        model = prop_models.Amenity
        fields = "__all__"
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
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"

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
    images = PropertyImageSerializer(many=True, read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    virtual_tours = PropertyVirtualTourSerializer(many=True, read_only=True)
    virtual_tours_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = prop_models.Property
        fields = ["id","property_category","agent","address","is_residential","description",\
            "added_on","education_facility","transport_facility","point_of_interest","amenity",\
            "images","videos","virtual_tours", "images_count","videos_count","virtual_tours_count"]

        extra_kwargs = {'added_on': {'read_only': True}, 'agent': {'read_only': True},\
                        'education_facility': {'read_only': True},'transport_facility': {'read_only': True},'point_of_interest': {'read_only': True},\
                            'amenity': {'read_only': True},'images': {'read_only': True},'images_count': {'read_only': True},\
                                'videos': {'read_only': True},'videos_count': {'read_only': True},'virtual_tours': {'read_only': True},\
                                    'virtual_tours_count': {'read_only': True},'address': {'read_only': True}}

    def get_images_count(self, instance):
        return instance.images.count()
    
    def get_videos_count(self, instance):
        return instance.videos.count()

    def get_virtual_tours_count(self, instance):
        return instance.virtual_tours.count()

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyFileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyFileLabel
        fields = "__all__"
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
